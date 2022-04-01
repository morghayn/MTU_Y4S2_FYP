#!/usr/bin/env bash

HOST_ADDRESS=$(echo "$host_address"  | sed -n 's/nameserver //p' /etc/resolv.conf)
sed -i "/^DATABASE_HOST=/s/=.*/=\"$HOST_ADDRESS\"/" .env