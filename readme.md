# Secure Coding

Tiny Shopping Mall Website.

You should add some functions and complete the security requirements.

## requirements

if you don't have a miniconda(or anaconda), you can install it on this url.
https://docs.anaconda.com/free/miniconda/index.html

```
conda create -n secure_coding python=3.9
conda activate secure_coding
pip install streamlit
pip install fastapi uvicorn
```

## usage

run the front and backend processes.

```
streamlit run streamlit_app.py
uvicorn fastapi_app:app --reload
```

if you want to test on external machine, you can utilize the ngrok to forwarding the url.
```
# optional
ngrok http 8501
```