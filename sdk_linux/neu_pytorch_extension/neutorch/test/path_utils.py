import os
import platform


def get_model_path(model_name):
    if platform.system() == "Linux":
        return f"/data/models/{model_name}"
    elif platform.system() == "Windows":
        if os.path.exists("C:/data/models"):
            return f"C:/data/models/{model_name}"
        elif os.path.exists("D:/data/models"):
            return f"D:/data/models/{model_name}"
    else:
        raise NotImplementedError("Unsupported operating system")


def get_data_path():
    if platform.system() == "Linux":
        return f"/data/"
    elif platform.system() == "Windows":
        if os.path.exists("C:/data/"):
            return f"C:/data/"
        elif os.path.exists("D:/data/"):
            return f"D:/data/"
        else:
            raise FileNotFoundError("Neither C:/data/ nor D:/data/ exists")
    else:
        raise NotImplementedError("Unsupported operating system")
