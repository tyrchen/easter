TARGET = display
TMP_COFFEE = _${TARGET}.coffee~
TMP_JS = _${TARGET}.js
COMPILER = coffee
ASSET_PATH = ../../static/assets
OUTPUT = ${ASSET_PATH}/${TARGET}.js
FILENAMES = application helper controllers views
FILES = $(patsubst %, %.coffee, $(FILENAMES))

build:
	@cat ${FILES} > ${TMP_COFFEE}
	@$(COMPILER) -c ${TMP_COFFEE}
	@rm ${TMP_COFFEE}
	@mv ${TMP_JS} ${OUTPUT}
	@echo "${OUTPUT} is built successfully."