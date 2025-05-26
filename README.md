# usragnt
This tool extracts the [User Agent](https://51degrees.com/blog/understanding-user-agent-string)  field from JSON logs, passes it to [useragentstrings.com](https://useragentstring.com/) API and returns the browser and its version and the OS and its version aswell. This can be forked and edited to accept all values that the API provides.  


### Useage
```bash
python3 usragnt.py {path/to/logfile}
```

---
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)