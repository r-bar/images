local images = import 'images.json';

local project_repo_resources = [
  {
    name: '%(project)s:%(tag)s@registry-image' % img,
    type: 'registry-image',
    icon: 'docker',
    source: {
      repository: img.repository,
      tag: img.tag,
      username: '((registry.username))',
      password: '((registry.password))',
    },
  }
  for img in images
];

local project_jobs = [
  {
    name: 'build-%(project)s-%(tag)s' % img,
    plan: [
      {
        get: 'git-repo',
        trigger: true,
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
            DOCKERFILE: 'git-repo/images/%(project)s/Dockerfile' % img,
            CONTEXT: 'git-repo/images/%(project)s/files' % img,
            BUILD_ARGS_FILE: 'git-repo/images/%(project)s/tags/%(tag)s' % img,
          },
          run: {
            path: 'build',
          },
        },
      },
      {
        put: '%(project)s:%(tag)s@registry-image' % img,
        params: {
          image: 'image/image.tar',
        },
      },
    ],
  }
  for img in images
];

{
  resource_types: [],
  resources: project_repo_resources + [
    {
      name: 'git-repo',
      icon: 'github',
      type: 'git',
      source: {
        uri: 'git@github.com:r-bar/images.git',
        branch: 'master',
        private_key: '((git-config.ssh-private-key))',
      },
      webhook_token: '((webhook-token))',
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
  jobs: project_jobs,
}
