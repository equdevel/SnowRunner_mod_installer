import os
import sys
import msvcrt
from dotenv import load_dotenv
import shutil
import requests
import json
from tqdm import tqdm
import argparse
from glob import glob
from json.decoder import JSONDecodeError

import mod_installer
