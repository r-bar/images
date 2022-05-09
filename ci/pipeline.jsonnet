local image_repo_resource = function(img) {
  name: '%(image)s-%(tag)s-registry-image' % img,
  type: 'registry-image',
  icon: 'docker',
  source: {
    repository: img.repository,
    tag: img.tag,
    username: '((registry.username))',
    password: '((registry.password))',
  },
};

local image_job = function(img) {
  name: 'build-%(image)s-%(tag)s' % img,
  plan: [
    {
      get: 'git-repo',
      trigger: true,
      passed: ['update-pipeline'],
    },
    {
      task: 'build',
      privileged: true,
      config: {
        platform: 'linux',
        image_resource: {
          type: 'registry-image',
          source: { repository: 'concourse/oci-build-task' },
        },
        inputs: [{ name: 'git-repo' }],
        outputs: [{ name: 'image' }],
        params: {
          DOCKERFILE: 'git-repo/images/%(image)s/Dockerfile' % img,
          CONTEXT: 'git-repo/images/%(image)s/files' % img,
          BUILD_ARGS_FILE: 'git-repo/images/%(image)s/tags/%(tag)s' % img,
        },
        run: {
          path: 'build',
        },
      },
    },
    {
      put: image_repo_resource(img).name,
      params: {
        image: 'image/image.tar',
      },
    },
  ],
};

function(images) {
  resource_types: [],
  resources: [image_repo_resource(img) for img in images] + [
    {
      name: 'git-repo',
      icon: 'github',
      type: 'git',
      source: {
        uri: 'git@github.com:r-bar/images.git',
        branch: 'master',
        private_key: '((git-config.ssh-private-key))',
      },
      webhook_token: '((git-config.webhook-token))',
      check_every: '24h',
    },
    //{
    //  name: 'build-status',
    //  type: 'github-status',
    //  icon: 'list-status',
    //  source: {
    //    owner: 'r-bar',
    //    repository: 'images',
    //    access_token: '((github-access-token))',
    //  },
    //},
  ],
  jobs: [
    {
      name: 'update-pipeline',
      plan: [
        {
          get: 'git-repo',
          trigger: true,
        },
        {
          task: 'build-pipeline.json',
          config: {
            platform: 'linux',
            image_resource: {
              type: 'registry-image',
              source: {
                repository: 'registry.barth.tech/docker.io/library/python',
                tag: '3.10-alpine',
              },
            },
            inputs: [{ name: 'git-repo' }],
            outputs: [{ name: 'git-repo' }],
            run: {
              path: 'ash',
              args: [
                '-c',
                |||
                  set -e
                  apk add -q --no-progress make jsonnet
                  cd git-repo
                  ls images
                  make ci/pipeline.json
                  cat ci/pipeline.json
                |||,
              ],
            },
          },
        },
        {
          set_pipeline: 'self',
          file: 'git-repo/ci/pipeline.json',
        },
      ],
    },
  ] + [image_job(img) for img in images],
}
