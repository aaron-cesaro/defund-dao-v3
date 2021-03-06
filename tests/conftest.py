import pytest


@pytest.fixture()
def TOKEN_URI():
    return "data:application/json;base64,eyJuYW1lIjoiRGVmdW5kIFBhc3MiLCAiZGVzY3JpcHRpb24iOiJEZUZ1bmQgUGFzcyIsICJpbWFnZSI6Imh0dHBzOi8vaXBmcy5pby9pcGZzL1FtVFdOblI2MlIzd2U2THFTV0szdXExRUQ4SGhWczdLRTlYc1dENGJ2TXY5aG0/ZmlsZW5hbWU9dmVudHVyZS5qcGVnIiwgImF0dHJpYnV0ZXMiOiBbIHsidHJhaXRfdHlwZSI6Ik1lbWJlcnNoaXAiLCAidmFsdWUiOiJTdGFuZGFyZCJ9LHsidHJhaXRfdHlwZSI6IlJvbGUiLCAidmFsdWUiOiJJbnZlc3RvciJ9XX0="


@pytest.fixture()
def VENTURE_LEAGUE_ROLES():
    return ["ANALYST", "ASSOCIATE"]


@pytest.fixture()
def IMAGE_PATH():
    return "./img/{}.jpeg"


@pytest.fixture()
def STANDARD_PASS_IMAGE():
    return "https://ipfs.io/ipfs/iuhO&BUIOYBiuybiuYUvUOYo/?filename=standard.jpeg"


@pytest.fixture()
def LEAGUE_PASS_IMAGE():
    return "https://ipfs.io/ipfs/iuhO&BUIOYBiuybiuYUvUOYo/?filename=league.jpeg"
