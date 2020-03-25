import requests
import json, base64
import os

class BlockChainWriter():
    __instance = None
    def __init__(self, config_file):
        if BlockChainWriter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            BlockChainWriter.__instance = self
            assert os.path.isfile(config_file), Exception("%s does not exist. Please enter a valid file" % (config_file))
            with open(config_file, "r") as f:
                config = json.loads(f.read())
                for key in ["block_chain_url", "case_name", "file_unique_id", "examiner_name", "information", "output_dir"]:
                    assert key in config.keys(), Exception("The configuration file in not valid!")
            self.config = config
            self.url = config["block_chain_url"]

    @staticmethod
    def getBlockchainWriter():
        return BlockChainWriter.__instance

    def Set_hash(self, md5, sha1, sha256):
        self.md5 = md5
        self.sha1 = sha1
        self.sha256 = sha256
        self.config["md5"] = md5
        self.config["sha1"] = sha1
        self.config["sha256"] = sha256

    def Write_to_blockChain(self, file_name):
        self.config["file_name"] = file_name

        self.r = requests.post(self.url, data=self.config)
        self.c = json.loads(self.r.content.decode("utf-8"))

        if self.config["output_dir"] != "":
            os.chdir(self.config["output_dir"])
        with open(self.c["name"], "wb") as f:
            f.write(base64.b64decode(self.c["pdf"]))
        print(self.c["qr_data"])
        return self.c["qr_data"]



if __name__ == '__main__':
    post = {
        "md5": "15ccf889015e686a8c42d8c6fd8988b4",
        "sha1": "48690a0c7aba71cf2957eca6a4eedd5f0f86554f",
        "sha256": "b94b8050e161da332a38d02f40deb67dfdf395bdd1e36ab1cffead8e9b807255",
        "case_name": "test_case",
        "file_unique_id": "P001",
        "examiner_name": "Tim",
        "information": "test photography"
    }

    url = "http://127.0.0.1:8000/registreAPI"

    r = requests.post(url, data=post)
    c = json.loads(r.content.decode("utf-8"))

    os.chdir(r"C:/Users/Tim/Downloads")
    with open(c["name"], "wb") as f:
        f.write(base64.b64decode(c["pdf"]))

    print(c["qr_data"])