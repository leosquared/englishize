update:
ifdef filepath
	aws lambda update-function-code --function-name englishize --zip-file fileb://$(filepath)
else
	echo "using file $$(ls aws-lambda/*.zip)"
	aws lambda update-function-code --function-name englishize --zip-file "fileb://$$(ls aws-lambda/*.zip)"
endif

new-function:
	cd aws-lambda/ENV/lib/python3.7/site-packages/ && \
	zip -q -r9 ../../../../function.zip . && \
	cd ../../../.. && \
	zip -q -g function.zip translate.py && \
	cd ..	

test:
	echo "$$(pwd)"
