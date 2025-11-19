# curl

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/network_tools/curl.md) \]

## I. Overview

openvela provides a built-in curl tool, a command-line-based file transfer utility. curl supports file upload and download through URL syntax, making it a comprehensive transfer solution. Additionally, curl includes the libcurl library designed for software development, which enables building applications based on HTTP, FTP, and other protocols.

## II. Configuration Instructions

Before using the curl tool, enable the following options in the configuration file:

```Makefile
CONFIG_LIB_ZLIB=y
CONFIG_CRYPTO_MBEDTLS=y
CONFIG_LIB_CURL=y
CONFIG_UTILS_CURL=y
```

> **Note**: Ensure these options are properly configured to meet the dependencies required for the curl tool.

## III. Common Use Cases

The `curl` tool can be used for file downloads, network performance testing, and more. Below are typical scenarios and operational steps.

### 1. Downloading Files

#### Prerequisites

The openvela-equipped device and PC must connect to the same router (wired or wireless).

#### Operation Steps

1. Start an HTTP server on the PC. Run one of the following commands based on your Python version:

    - For Python 2:

        ```bash
        python -m SimpleHTTPServer
        ```

    - For Python 3+:

        ```bash
        python -m http.server
        ```

    This will start an HTTP server using the current directory as the root.

2. Prepare the file for transfer.

    Place the target file (e.g., ota.zip) in the directory where the Python command is executed.

3. Connect the openvela device to the router via Wi-Fi.

    Run the following commands on the device:

    ```Bash
    ifup wlan0
    wapi mode wlan0 2
    wapi psk wlan0 <YOUR_WIFI_PASSWORD> 3 # # Replace with Wi-Fi password
    wapi essid wlan0 <YOUR_WIFI_NAME> 1  # Replace with Wi-Fi SSID
    renew wlan0
    ```

4. Download the file from the HTTP server.

    Execute this command on the device:

    **Note**: Replace `YOUR_FILE_SERVER_IP` with the PC's IP address. This saves `ota.zip` to `/data/ota.zip`.

    ```Bash
    curl -o /data/ota.zip http://<YOUR_FILE_SERVER_IP>:8000/ota.zip &
    ```

### 2. Uploading Device Files

Follow these steps to upload files from the device to a local PC using curl.

#### Operation Steps

1. Prepare an upload script.

    Create a Python script upload.py on the PC:

    ```Python
    #!/bin/env python3

    import os, shutil, uvicorn, socket
    from fastapi import FastAPI, File, UploadFile

    app = FastAPI()

    @app.post("/upload/")
    async def create_upload_file(file: UploadFile = File(...)):
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename}


    def my_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip


    if __name__ == "__main__":
        print("curl -X POST -F file=@./a.log %s:4321/upload/" % my_ip())
        uvicorn.run(app, host="0.0.0.0", port=4321)
    ```

2. Install dependencies.

    Run on the PC:

    ```Bash
    # Install Python dependencies
    pip install uvicorn fastapi python-multipart
    ```

3. Run the upload script.

    ```Bash
    # Execute upload.py
    sudo chmod 777 upload.py

    ./upload.py
    ```

    The script will print a `curl` command template, for example:

    ```Bash
    curl -X POST -F file=@./a.log <PC_IP>:4321/upload/
    ```

4. Upload the device file.

    On the connected device, run:

    ```Bash
    curl -X POST -F file=@/data/trace.log http://<PC_IP>:4321/upload/
    ```

    - `/data/trace.log`: Path to the file on the device.
    - `<PC_IP>`: The PC's IP address displayed by the script.

5. Notes.

    - If the upload fails, check the PC's network configuration, confirm the PC's WAN IP and update <PC_IP> in the command.

        ```bash
        ifconfig
        ```

    - Ensure the device and PC are on the same network, and port `4321` is unblocked.

### 3. Retrieving Web Content

Use `curl` to fetch and print webpage content:

```Bash
curl www.example.com
```

> **Note**
>
> This sends a GET request to `www.example.com` and prints the response. Replace `www.example.com` with the target URL.

### 4. Fetching Network Files with Redirects

Use the -L flag to follow redirects:

```Bash
curl -L -o /data/test.mp3 https://example.com
```

#### Key Considerations

1. Example:

    - `https://example.com` is a placeholder. Replace it with the actual download link.
    - `/data/test.mp3` is the output path. Modify it as needed.

2. Redirect Handling:

    Use `-L` to automatically follow redirects and fetch the final file.

3. URL Format:

    - When running on a device, do not use quotation marks around the URL.
    - When running on a PC, URLs can use quotation marks.

4. Special Character Escaping:

    | **Original** | **Escaped** |
    | ------------ | ----------- |
    | +            | %2B         |
    | Space        | %20         |
    | /            | %2F         |
    | ?            | %3F         |
    | %            | %25         |
    | &            | %26         |
    | =            | %3D         |
    | #            | %23         |

### 5. Network Performance Testing

Measure TCP/SSL handshake times with -w.

#### Examples

```Bash
curl -w "TCP handshake: %{time_connect}, SSL handshake: %{time_appconnect}\n" -so /dev/null <https://speech-preview.example.com/>
```

#### Sample Output

```Bash
TCP handshake: 0.035127, SSL handshake: 0.500842
```

- TCP handshake: Time taken for TCP three-way handshake.
- SSL handshake: Time taken for SSL/TLS handshake.

## IV. Parameter Reference

Full list of curl parameters (run curl --help all for details):

```Shell
curl --help all
Usage: curl [options...] <url>
     --abstract-unix-socket <path> Connect via abstract Unix domain socket
     --alt-svc <file name> Enable alt-svc with this cache file
     --anyauth            Pick any authentication method
 -a, --append             Append to target file when uploading
     --aws-sigv4 <provider1[:provider2[:region[:service]]]> Use AWS V4 signature authentication
     --basic              Use HTTP Basic Authentication
     --cacert <file>      CA certificate to verify peer against
     --capath <dir>       CA directory to verify peer against
 -E, --cert <certificate[:password]> Client certificate file and password
     --cert-status        Verify the status of the server cert via OCSP-staple
     --cert-type <type>   Certificate type (DER/PEM/ENG/P12)
     --ciphers <list of ciphers> SSL ciphers to use
     --compressed         Request compressed response
     --compressed-ssh     Enable SSH compression
 -K, --config <file>      Read config from a file
     --connect-timeout <fractional seconds> Maximum time allowed for connection
     --connect-to <HOST1:PORT1:HOST2:PORT2> Connect to host
 -C, --continue-at <offset> Resumed transfer offset
 -b, --cookie <data|filename> Send cookies from string/file
 -c, --cookie-jar <filename> Write cookies to <filename> after operation
     --create-dirs        Create necessary local directory hierarchy
     --create-file-mode <mode> File mode for created files
     --crlf               Convert LF to CRLF in upload
     --crlfile <file>     Use this CRL list
     --curves <algorithm list> (EC) TLS key exchange algorithm(s) to request
 -d, --data <data>        HTTP POST data
     --data-ascii <data>  HTTP POST ASCII data
     --data-binary <data> HTTP POST binary data
     --data-raw <data>    HTTP POST data, '@' allowed
     --data-urlencode <data> HTTP POST data URL encoded
     --delegation <LEVEL> GSS-API delegation permission
     --digest             Use HTTP Digest Authentication
 -q, --disable            Disable .curlrc
     --disable-eprt       Inhibit using EPRT or LPRT
     --disable-epsv       Inhibit using EPSV
     --disallow-username-in-url Disallow username in URL
     --dns-interface <interface> Interface to use for DNS requests
     --dns-ipv4-addr <address> IPv4 address to use for DNS requests
     --dns-ipv6-addr <address> IPv6 address to use for DNS requests
     --dns-servers <addresses> DNS server addrs to use
     --doh-cert-status    Verify the status of the DoH server cert via OCSP-staple
     --doh-insecure       Allow insecure DoH server connections
     --doh-url <URL>      Resolve host names over DoH
 -D, --dump-header <filename> Write the received headers to <filename>
     --egd-file <file>    EGD socket path for random data
     --engine <name>      Crypto engine to use
     --etag-compare <file> Pass an ETag from a file as a custom header
     --etag-save <file>   Parse ETag from a request and save it to a file
     --expect100-timeout <seconds> How long to wait for 100-continue
 -f, --fail               Fail fast with no output on HTTP errors
     --fail-early         Fail on first transfer error, do not continue
     --fail-with-body     Fail on HTTP errors but save the body
     --false-start        Enable TLS False Start
 -F, --form <name=content> Specify multipart MIME data
     --form-escape        Escape multipart form field/file names using backslash
     --form-string <name=string> Specify multipart MIME data
     --ftp-account <data> Account data string
     --ftp-alternative-to-user <command> String to replace USER [name]
     --ftp-create-dirs    Create the remote dirs if not present
     --ftp-method <method> Control CWD usage
     --ftp-pasv           Use PASV/EPSV instead of PORT
 -P, --ftp-port <address> Use PORT instead of PASV
     --ftp-pret           Send PRET before PASV
     --ftp-skip-pasv-ip   Skip the IP address for PASV
     --ftp-ssl-ccc        Send CCC after authenticating
     --ftp-ssl-ccc-mode <active/passive> Set CCC mode
     --ftp-ssl-control    Require SSL/TLS for FTP login, clear for transfer
 -G, --get                Put the post data in the URL and use GET
 -g, --globoff            Disable URL sequences and ranges using {} and []
     --happy-eyeballs-timeout-ms <milliseconds> Time for IPv6 before trying IPv4
     --haproxy-protocol   Send HAProxy PROXY protocol v1 header
 -I, --head               Show document info only
 -H, --header <header/@file> Pass custom header(s) to server
 -h, --help <category>    Get help for commands
     --hostpubmd5 <md5>   Acceptable MD5 hash of the host public key
     --hostpubsha256 <sha256> Acceptable SHA256 hash of the host public key
     --hsts <file name>   Enable HSTS with this cache file
     --http0.9            Allow HTTP 0.9 responses
 -0, --http1.0            Use HTTP 1.0
     --http1.1            Use HTTP 1.1
     --http2              Use HTTP 2
     --http2-prior-knowledge Use HTTP 2 without HTTP/1.1 Upgrade
     --http3              Use HTTP v3
     --ignore-content-length Ignore the size of the remote resource
 -i, --include            Include protocol response headers in the output
 -k, --insecure           Allow insecure server connections
     --interface <name>   Use network INTERFACE (or address)
 -4, --ipv4               Resolve names to IPv4 addresses
 -6, --ipv6               Resolve names to IPv6 addresses
     --json <data>        HTTP POST JSON
 -j, --junk-session-cookies Ignore session cookies read from file
     --keepalive-time <seconds> Interval time for keepalive probes
     --key <key>          Private key file name
     --key-type <type>    Private key file type (DER/PEM/ENG)
     --krb <level>        Enable Kerberos with security <level>
     --libcurl <file>     Dump libcurl equivalent code of this command line
     --limit-rate <speed> Limit transfer speed to RATE
 -l, --list-only          List only mode
     --local-port <num/range> Force use of RANGE for local port numbers
 -L, --location           Follow redirects
     --location-trusted   Like --location, and send auth to other hosts
     --login-options <options> Server login options
     --mail-auth <address> Originator address of the original email
     --mail-from <address> Mail from this address
     --mail-rcpt <address> Mail to this address
     --mail-rcpt-allowfails Allow RCPT TO command to fail for some recipients
 -M, --manual             Display the full manual
     --max-filesize <bytes> Maximum file size to download
     --max-redirs <num>   Maximum number of redirects allowed
 -m, --max-time <fractional seconds> Maximum time allowed for transfer
     --metalink           Process given URLs as metalink XML file
     --negotiate          Use HTTP Negotiate (SPNEGO) authentication
 -n, --netrc              Must read .netrc for user name and password
     --netrc-file <filename> Specify FILE for netrc
     --netrc-optional     Use either .netrc or URL
 -:, --next               Make next URL use its separate set of options
     --no-alpn            Disable the ALPN TLS extension
 -N, --no-buffer          Disable buffering of the output stream
     --no-clobber         Do not overwrite files that already exist
     --no-keepalive       Disable TCP keepalive on the connection
     --no-npn             Disable the NPN TLS extension
     --no-progress-meter  Do not show the progress meter
     --no-sessionid       Disable SSL session-ID reusing
     --noproxy <no-proxy-list> List of hosts which do not use proxy
     --ntlm               Use HTTP NTLM authentication
     --ntlm-wb            Use HTTP NTLM authentication with winbind
     --oauth2-bearer <token> OAuth 2 Bearer Token
 -o, --output <file>      Write to file instead of stdout
     --output-dir <dir>   Directory to save files in
 -Z, --parallel           Perform transfers in parallel
     --parallel-immediate Do not wait for multiplexing (with --parallel)
     --parallel-max <num> Maximum concurrency for parallel transfers
     --pass <phrase>      Pass phrase for the private key
     --path-as-is         Do not squash .. sequences in URL path
     --pinnedpubkey <hashes> FILE/HASHES Public key to verify peer against
     --post301            Do not switch to GET after following a 301
     --post302            Do not switch to GET after following a 302
     --post303            Do not switch to GET after following a 303
     --preproxy [protocol://]host[:port] Use this proxy first
 -#, --progress-bar       Display transfer progress as a bar
     --proto <protocols>  Enable/disable PROTOCOLS
     --proto-default <protocol> Use PROTOCOL for any URL missing a scheme
     --proto-redir <protocols> Enable/disable PROTOCOLS on redirect
 -x, --proxy [protocol://]host[:port] Use this proxy
     --proxy-anyauth      Pick any proxy authentication method
     --proxy-basic        Use Basic authentication on the proxy
     --proxy-cacert <file> CA certificate to verify peer against for proxy
     --proxy-capath <dir> CA directory to verify peer against for proxy
     --proxy-cert <cert[:passwd]> Set client certificate for proxy
     --proxy-cert-type <type> Client certificate type for HTTPS proxy
     --proxy-ciphers <list> SSL ciphers to use for proxy
     --proxy-crlfile <file> Set a CRL list for proxy
     --proxy-digest       Use Digest authentication on the proxy
     --proxy-header <header/@file> Pass custom header(s) to proxy
     --proxy-insecure     Do HTTPS proxy connections without verifying the proxy
     --proxy-key <key>    Private key for HTTPS proxy
     --proxy-key-type <type> Private key file type for proxy
     --proxy-negotiate    Use HTTP Negotiate (SPNEGO) authentication on the proxy
     --proxy-ntlm         Use NTLM authentication on the proxy
     --proxy-pass <phrase> Pass phrase for the private key for HTTPS proxy
     --proxy-pinnedpubkey <hashes> FILE/HASHES public key to verify proxy with
     --proxy-service-name <name> SPNEGO proxy service name
     --proxy-ssl-allow-beast Allow security flaw for interop for HTTPS proxy
     --proxy-ssl-auto-client-cert Use auto client certificate for proxy (Schannel)
     --proxy-tls13-ciphers <ciphersuite list> TLS 1.3 proxy cipher suites
     --proxy-tlsauthtype <type> TLS authentication type for HTTPS proxy
     --proxy-tlspassword <string> TLS password for HTTPS proxy
     --proxy-tlsuser <name> TLS username for HTTPS proxy
     --proxy-tlsv1        Use TLSv1 for HTTPS proxy
 -U, --proxy-user <user:password> Proxy user and password
     --proxy1.0 <host[:port]> Use HTTP/1.0 proxy on given port
 -p, --proxytunnel        Operate through an HTTP proxy tunnel (using CONNECT)
     --pubkey <key>       SSH Public key file name
 -Q, --quote <command>    Send command(s) to server before transfer
     --random-file <file> File for reading random data from
 -r, --range <range>      Retrieve only the bytes within RANGE
     --rate <max request rate> Request rate for serial transfers
     --raw                Do HTTP "raw"; no transfer decoding
 -e, --referer <URL>      Referrer URL
 -J, --remote-header-name Use the header-provided filename
 -O, --remote-name        Write output to a file named as the remote file
     --remote-name-all    Use the remote file name for all URLs
 -R, --remote-time        Set the remote file's time on the local output
     --remove-on-error    Remove output file on errors
 -X, --request <method>   Specify request method to use
     --request-target <path> Specify the target for this request
     --resolve <[+]host:port:addr[,addr]...> Resolve the host+port to this address
     --retry <num>        Retry request if transient problems occur
     --retry-all-errors   Retry all errors (use with --retry)
     --retry-connrefused  Retry on connection refused (use with --retry)
     --retry-delay <seconds> Wait time between retries
     --retry-max-time <seconds> Retry only within this period
     --sasl-authzid <identity> Identity for SASL PLAIN authentication
     --sasl-ir            Enable initial response in SASL authentication
     --service-name <name> SPNEGO service name
 -S, --show-error         Show error even when -s is used
 -s, --silent             Silent mode
     --socks4 <host[:port]> SOCKS4 proxy on given host + port
     --socks4a <host[:port]> SOCKS4a proxy on given host + port
     --socks5 <host[:port]> SOCKS5 proxy on given host + port
     --socks5-basic       Enable username/password auth for SOCKS5 proxies
     --socks5-gssapi      Enable GSS-API auth for SOCKS5 proxies
     --socks5-gssapi-nec  Compatibility with NEC SOCKS5 server
     --socks5-gssapi-service <name> SOCKS5 proxy service name for GSS-API
     --socks5-hostname <host[:port]> SOCKS5 proxy, pass host name to proxy
 -Y, --speed-limit <speed> Stop transfers slower than this
 -y, --speed-time <seconds> Trigger 'speed-limit' abort after this time
     --ssl                Try SSL/TLS
     --ssl-allow-beast    Allow security flaw to improve interop
     --ssl-auto-client-cert Use auto client certificate (Schannel)
     --ssl-no-revoke      Disable cert revocation checks (Schannel)
     --ssl-reqd           Require SSL/TLS
     --ssl-revoke-best-effort Ignore missing/offline cert CRL dist points
 -2, --sslv2              Use SSLv2
 -3, --sslv3              Use SSLv3
     --stderr <file>      Where to redirect stderr
     --styled-output      Enable styled output for HTTP headers
     --suppress-connect-headers Suppress proxy CONNECT response headers
     --tcp-fastopen       Use TCP Fast Open
     --tcp-nodelay        Use the TCP_NODELAY option
 -t, --telnet-option <opt=val> Set telnet option
     --tftp-blksize <value> Set TFTP BLKSIZE option
     --tftp-no-options    Do not send any TFTP options
 -z, --time-cond <time>   Transfer based on a time condition
     --tls-max <VERSION>  Set maximum allowed TLS version
     --tls13-ciphers <ciphersuite list> TLS 1.3 cipher suites to use
     --tlsauthtype <type> TLS authentication type
     --tlspassword <string> TLS password
     --tlsuser <name>     TLS user name
 -1, --tlsv1              Use TLSv1.0 or greater
     --tlsv1.0            Use TLSv1.0 or greater
     --tlsv1.1            Use TLSv1.1 or greater
     --tlsv1.2            Use TLSv1.2 or greater
     --tlsv1.3            Use TLSv1.3 or greater
     --tr-encoding        Request compressed transfer encoding
     --trace <file>       Write a debug trace to FILE
     --trace-ascii <file> Like --trace, but without hex output
     --trace-time         Add time stamps to trace/verbose output
     --unix-socket <path> Connect through this Unix domain socket
 -T, --upload-file <file> Transfer local FILE to destination
     --url <url>          URL to work with
 -B, --use-ascii          Use ASCII/text transfer
 -u, --user <user:password> Server user and password
 -A, --user-agent <name>  Send User-Agent <name> to server
 -v, --verbose            Make the operation more talkative
 -V, --version            Show version number and quit
 -w, --write-out <format> Use output FORMAT after completion
     --xattr              Store metadata in extended file attributes
```
