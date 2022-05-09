image_files = $(shell find images)

ci/images.json: ${image_files} build.py
	./build.py images | tee $@

ci/pipeline.json: ci/images.json ci/pipeline.jsonnet
	jsonnet --tla-code-file images=ci/images.json ci/pipeline.jsonnet -o $@

debug:
	echo ${image_files}
