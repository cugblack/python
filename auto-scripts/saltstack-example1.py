#!/usr/bin/env python
import salt.client
client = salt.client.LocalClient()
ret = client.cmd('*', 'test.ping')
print ret
