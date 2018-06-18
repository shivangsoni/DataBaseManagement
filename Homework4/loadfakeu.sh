#!/bin/bash

if [ $# -eq "0" ]
	then 
		python FakeUData.py
	else
		python FakeUData.py $1
fi

