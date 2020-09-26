CHART_PIPLINES = $(shell find . -name pipeline.yaml ! -path './ci/*')
ci/full-pipeline.yaml: ci/pipeline.yaml ${CHART_PIPLINES}
	@python3 ci/merge-pipelines.py $^ | tee $@
