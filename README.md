# ICS-Sniper Modbus-U Software Testbed

**SWaT software testbed (Unconnected Modbus version)**

This repository contains the software-only Modbus/TCP testbed used by ICS-Sniper. Six simulated PLCs and the SCADA application run on Linux hosts and communicate through an OpenVPN router.

Replace every value in angle brackets, such as `<router-public-ip>`, with a value from your environment. Generate new VPN credentials for every deployment.

## Architecture

```text
Software PLC host                OpenVPN router                 SCADA host
OpenVPN: 10.8.0.2/24  <------->  OpenVPN: 10.8.0.1/24  <----> OpenVPN: 10.8.0.3/24
PLC servers: TCP 503-508                                      SCADA: TCP 502
```

## Requirements

The testbed uses three Linux instances. The table lists the baseline configuration used for the original deployment; increase storage when collecting long packet captures.

| Instance | Quantity | Operating system | Suggested baseline | Network and access requirements |
| --- | ---: | --- | --- | --- |
| OpenVPN router | 1 | Ubuntu 22.04 | 1 vCPU, 1 GiB RAM, 32 GiB storage | Publicly reachable TCP 1194; SSH access; IP forwarding; a public IP or DNS name |
| SCADA | 1 | Ubuntu 22.04 | 4 vCPUs, 16 GiB RAM, 32 GiB storage | SSH access; outbound TCP access to the router; TCP 502 available locally |
| Software PLC host | 1 | Ubuntu 22.04 | 8 vCPUs, 32 GiB RAM, 32 GiB storage | SSH access; outbound TCP access to the router; TCP 503-508 available locally |

The router firewall or cloud security group must allow TCP 1194 from both VPN clients.

## Clone the Repository

Clone the public repository on the SCADA and software PLC hosts.

```bash
cd /home/ubuntu
git clone https://github.com/ICS-Sniper/Modbus-U-software-testbed.git
cd Modbus-U-software-testbed
```

## One-Time Setup

### 1. Configure the OpenVPN router

Log in to the router and install OpenVPN and Easy-RSA:

```bash
sudo apt update
sudo apt install -y easy-rsa openvpn
mkdir -p ~/openvpn-ca
cd ~/openvpn-ca
```

Create the certificate authority and server material:

```bash
/usr/share/easy-rsa/easyrsa init-pki
/usr/share/easy-rsa/easyrsa build-ca
/usr/share/easy-rsa/easyrsa gen-req server nopass
/usr/share/easy-rsa/easyrsa sign-req server server
/usr/share/easy-rsa/easyrsa gen-dh
openvpn --genkey tls-crypt-v2-server ta.key
```

Create separate credentials for the software PLC and SCADA clients:

```bash
/usr/share/easy-rsa/easyrsa gen-req plc-gateway nopass
/usr/share/easy-rsa/easyrsa sign-req client plc-gateway
openvpn --tls-crypt-v2 ./ta.key \
  --genkey tls-crypt-v2-client ./pki/private/plc-gateway-tc.key

/usr/share/easy-rsa/easyrsa gen-req scada nopass
/usr/share/easy-rsa/easyrsa sign-req client scada
openvpn --tls-crypt-v2 ./ta.key \
  --genkey tls-crypt-v2-client ./pki/private/scada-tc.key
```

Install the server material:

```bash
sudo install -d -m 0755 /etc/openvpn/ccd
sudo install -m 0644 ~/openvpn-ca/pki/ca.crt /etc/openvpn/ca.crt
sudo install -m 0644 ~/openvpn-ca/pki/dh.pem /etc/openvpn/dh.pem
sudo install -m 0644 ~/openvpn-ca/pki/issued/server.crt /etc/openvpn/server.crt
sudo install -m 0600 ~/openvpn-ca/pki/private/server.key /etc/openvpn/server.key
sudo install -m 0600 ~/openvpn-ca/ta.key /etc/openvpn/ta.key
```

Create `/etc/openvpn/server.conf`:

```conf
port 1194
proto tcp
dev tun

ca ca.crt
cert server.crt
key server.key
dh dh.pem
tls-crypt-v2 /etc/openvpn/ta.key

server 10.8.0.0 255.255.255.0
topology subnet
client-config-dir /etc/openvpn/ccd
ifconfig-pool-persist ipp.txt
push "route 10.8.0.0 255.255.255.0"

keepalive 10 120
persist-key
persist-tun
cipher AES-256-GCM
auth SHA256
auth-nocache
user nobody
group nogroup
status openvpn-status.log
verb 3
```

Assign stable VPN addresses:

```bash
echo "ifconfig-push 10.8.0.2 255.255.255.0" | \
  sudo tee /etc/openvpn/ccd/plc-gateway >/dev/null
echo "ifconfig-push 10.8.0.3 255.255.255.0" | \
  sudo tee /etc/openvpn/ccd/scada >/dev/null
```

To run the testbed only on demand, disable automatic startup:

```bash
sudo systemctl disable openvpn
sudo systemctl disable openvpn@server
```

### 2. Configure the Linux VPN clients

Run the following on both the SCADA and software PLC hosts:

```bash
sudo apt update
sudo apt install -y openvpn
mkdir -p ~/openvpn-ca
chmod 700 ~/openvpn-ca
```

Securely copy the following files from the router. Never transfer private keys through a public repository or shared public storage.

| Client | Router source | Client destination |
| --- | --- | --- |
| PLC | `pki/ca.crt` | `ca.crt` |
| PLC | `pki/issued/plc-gateway.crt` | `plc-gateway.crt` |
| PLC | `pki/private/plc-gateway.key` | `plc-gateway.key` |
| PLC | `pki/private/plc-gateway-tc.key` | `plc-gateway-tc.key` |
| SCADA | `pki/ca.crt` | `ca.crt` |
| SCADA | `pki/issued/scada.crt` | `scada.crt` |
| SCADA | `pki/private/scada.key` | `scada.key` |
| SCADA | `pki/private/scada-tc.key` | `scada-tc.key` |

Protect the client private keys:

```bash
chmod 600 ~/openvpn-ca/*.key
```

On the software PLC host, create `~/openvpn-ca/client.conf`:

```conf
client
dev tun
proto tcp
remote <router-public-ip-or-dns> 1194
resolv-retry infinite
nobind
persist-key
persist-tun

ca ca.crt
cert plc-gateway.crt
key plc-gateway.key
remote-cert-tls server
tls-crypt-v2 plc-gateway-tc.key

pull
cipher AES-256-GCM
auth SHA256
auth-nocache
verb 3
```

On the SCADA host, create the same profile but use the SCADA credentials:

```conf
ca ca.crt
cert scada.crt
key scada.key
remote-cert-tls server
tls-crypt-v2 scada-tc.key
```

### 3. Install the Modbus software

Run these commands on both the SCADA and software PLC hosts:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
cd /home/ubuntu/Modbus-U-software-testbed
python3 -m venv .venv
.venv/bin/pip install \
  pymodbus==2.5.3 \
  pyserial-asyncio \
  cpppo==4.3.0 \
  numpy
```

PyModbus is installed from PyPI. The testbed-specific client and server entry
points remain in `modbus_helpers/` and are launched automatically by
`protocols.py`; do not copy them into the virtual environment.

Create the SCADA log directory on the SCADA host:

```bash
mkdir -p ~/test-setup/scadalogs
```

## Start the Testbed

Start the components in this order. Starting the PLCs before SCADA prints `SCADA main loop starts here` can cause initialization errors.

### 1. Start the router

```bash
ssh -i <ssh-key> ubuntu@<router-public-ip>
cd /etc/openvpn
sudo openvpn --config /etc/openvpn/server.conf --daemon
sudo sysctl -w net.ipv4.ip_forward=1
sudo ss -ltnp | grep 1194
```

### 2. Start SCADA

```bash
ssh -i <ssh-key> ubuntu@<scada-host>
cd ~/openvpn-ca
sudo openvpn --config client.conf --daemon
sudo sysctl -w net.ipv4.ip_forward=1
ping -c 3 10.8.0.1
ping -c 3 10.8.0.2
cd /home/ubuntu/Modbus-U-software-testbed
sudo .venv/bin/python SCADA_1.py
```

Wait for:

```text
SCADA main loop starts here
```

### 3. Start the software PLCs

In another terminal:

```bash
ssh -i <ssh-key> ubuntu@<software-plc-host>
cd ~/openvpn-ca
sudo openvpn --config client.conf --daemon
sudo sysctl -w net.ipv4.ip_forward=1
ping -c 3 10.8.0.1
ping -c 3 10.8.0.3
cd /home/ubuntu/Modbus-U-software-testbed
sudo .venv/bin/python plc_main.py
```

Keep the process in the foreground so initialization and communication errors remain visible.

## Optional Packet Capture

Install TShark on the router and create a trace directory:

```bash
sudo apt install -y tshark
mkdir -p ~/traces
```

Capture public-side and tunnel-side traffic in separate sessions:

```bash
sudo tshark -i <public-interface> -w ~/traces/public-side.pcap
```

```bash
sudo tshark -i tun0 -w ~/traces/tunnel-side.pcap
```

Use `ip link` to identify the public interface. Packet captures can contain sensitive traffic and should not be committed.

## Stop the Testbed

1. Stop `plc_main.py` with `Ctrl+C`.
2. Stop `SCADA_1.py` with `Ctrl+C`.
3. Stop OpenVPN on each Linux client with `sudo pkill openvpn`.
4. Stop OpenVPN on the router with `sudo pkill openvpn`.
5. Copy required logs or packet captures before terminating ephemeral instances.

## Troubleshooting

| Symptom | Likely cause | Check or fix |
| --- | --- | --- |
| VPN client reports `Connection refused` | Router OpenVPN process or TCP 1194 firewall rule is missing | Start the router service and check `sudo ss -ltnp \| grep 1194` |
| SCADA cannot bind TCP 502 | The process lacks permission or another server is running | Run with `sudo`; inspect `sudo ss -ltnp \| grep ':502'` |
| A script cannot find a Modbus helper | The repository checkout is incomplete | Confirm that `modbus_helpers/synch_client.py` and `modbus_helpers/servers.py` exist |
| SCADA cannot reach a software PLC | A VPN client is disconnected or received the wrong address | Check `ip addr`, the CCD filenames, and connectivity to `10.8.0.1` |
| OpenVPN assigns unexpected client addresses | Certificate common name does not match the CCD filename | Use the `plc-gateway` and `scada` certificate names shown above |

## Repository Layout

| Path | Purpose |
| --- | --- |
| `SCADA_1.py` | Modbus SCADA process |
| `plc_main.py` | Launcher for all six simulated PLCs |
| `plc/`, `plant/`, `controlblock/`, `logicblock/` | Software PLC and process simulation |
| `modbus_helpers/` | Testbed-specific Modbus client and server entry points |
| `tests/` | Testbed tests |
