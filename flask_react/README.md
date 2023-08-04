# local

`./launch_app2.sh`

```
curl --location http://127.0.0.1:5001/uploadFile --form 'file=@"./build/paul_graham_essay2.txt"'
curl -G http://127.0.0.1:5001/query?text=graham
```



# K8s

```
./build_and_push.sh
# OK
curl -G https://lahonda-ai-index.api.dev.ccs.guidewire.net/query?text=graham
curl -G https://lahonda-ai-index.api.dev.ccs.guidewire.net/getDocuments

curl -X POST -F "file=@./documents/paul_graham_essay.txt" https://lahonda-ai-index.api.dev.ccs.guidewire.net/upload/test
curl -X POST -F "file=@./documents/paul_graham_essay.txt" https://lahonda-ai-index.api.dev.ccs.guidewire.net/upload


