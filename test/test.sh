#!/bin/bash

touch test.log

pytest frontend > test.log

echo test.log
