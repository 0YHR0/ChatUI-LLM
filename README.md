# This is a skeleton project to deploy chat UI(chainlit) with the LLMs 
### Quick start
1. Set the UI config in .chainlit/config.toml
2. Set the LLM backend in config.yaml
3. Adjust the script to use the LLM 
   + locally: [local deploy](deploy_local.py)
    + remote api: [remote api](remote_api.py)

```shell
pip install -r requirements.txt
# If the pip install command does not work properly, you can substitute with the following commands
# pip install pyyaml
# pip install chainlit
# pip install torch
# pip install transformers


chainlit run app.py -w # hot loading
```







#### The example deploys [openai-community/gpt2](https://huggingface.co/openai-community/gpt2) locally

#### Please try with the long question more then 8 tokens.

![image-20240704152014843](https://markdown-1301334775.cos.eu-frankfurt.myqcloud.com/image-20240704152014843.png)

#### Refer to [Chainlit](https://github.com/Chainlit/chainlit)
