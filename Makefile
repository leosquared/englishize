update:
ifdef filepath
	aws lambda update-function-code --function-name englishize --zip-file fileb://$(filepath)
else
	echo "using file $$(ls aws-lambda/*.zip)"
	aws lambda update-function-code --function-name englishize --zip-file "fileb://$$(ls aws-lambda/*.zip)"
endif

test:
	echo "$$(pwd)"
