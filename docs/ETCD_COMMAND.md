# ETCD Commands

```bash
NAME:
        etcdctl - A simple command line client for etcd3.

USAGE:
        etcdctl [flags]

VERSION:
        3.5.5

API VERSION:
        3.5


COMMANDS:
        alarm disarm            Disarms all alarms
        alarm list              Lists all alarms
        auth disable            Disables authentication
        auth enable             Enables authentication
        auth status             Returns authentication status
        check datascale         Check the memory usage of holding data for different workloads on a given server endpoint.
        check perf              Check the performance of the etcd cluster
        compaction              Compacts the event history in etcd
        defrag                  Defragments the storage of the etcd members with given endpoints
        del                     Removes the specified key or range of keys [key, range_end)
        elect                   Observes and participates in leader election
        endpoint hashkv         Prints the KV history hash for each endpoint in --endpoints
        endpoint health         Checks the healthiness of endpoints specified in `--endpoints` flag
        endpoint status         Prints out the status of endpoints specified in `--endpoints` flag
        get                     Gets the key or a range of keys
        help                    Help about any command
        lease grant             Creates leases
        lease keep-alive        Keeps leases alive (renew)
        lease list              List all active leases
        lease revoke            Revokes leases
        lease timetolive        Get lease information
        lock                    Acquires a named lock
        make-mirror             Makes a mirror at the destination etcd cluster
        member add              Adds a member into the cluster
        member list             Lists all members in the cluster
        member promote          Promotes a non-voting member in the cluster
        member remove           Removes a member from the cluster
        member update           Updates a member in the cluster
        move-leader             Transfers leadership to another etcd cluster member.
        put                     Puts the given key into the store
        role add                Adds a new role
        role delete             Deletes a role
        role get                Gets detailed information of a role
        role grant-permission   Grants a key to a role
        role list               Lists all roles
        role revoke-permission  Revokes a key from a role
        snapshot restore        Restores an etcd member snapshot to an etcd directory
        snapshot save           Stores an etcd node backend snapshot to a given file
        snapshot status         [deprecated] Gets backend snapshot status of a given file
        txn                     Txn processes all the requests in one transaction
        user add                Adds a new user
        user delete             Deletes a user
        user get                Gets detailed information of a user
        user grant-role         Grants a role to a user
        user list               Lists all users
        user passwd             Changes password of user
        user revoke-role        Revokes a role from a user
        version                 Prints the version of etcdctl
        watch                   Watches events stream on keys or prefixes

OPTIONS:
      --cacert=""                               verify certificates of TLS-enabled secure servers using this CA bundle
      --cert=""                                 identify secure client using this TLS certificate file
      --command-timeout=5s                      timeout for short running command (excluding dial timeout)
      --debug[=false]                           enable client-side debug logging
      --dial-timeout=2s                         dial timeout for client connections
  -d, --discovery-srv=""                        domain name to query for SRV records describing cluster endpoints
      --discovery-srv-name=""                   service name to query when using DNS discovery
      --endpoints=[127.0.0.1:2379]              gRPC endpoints
  -h, --help[=false]                            help for etcdctl
      --hex[=false]                             print byte strings as hex encoded strings
      --insecure-discovery[=true]               accept insecure SRV records describing cluster endpoints
      --insecure-skip-tls-verify[=false]        skip server certificate verification (CAUTION: this option should be enabled only for testing purposes)
      --insecure-transport[=true]               disable transport security for client connections
      --keepalive-time=2s                       keepalive time for client connections
      --keepalive-timeout=6s                    keepalive timeout for client connections
      --key=""                                  identify secure client using this TLS key file
      --password=""                             password for authentication (if this option is used, --user option shouldn\'t include password)
      --user=""                                 username[:password] for authentication (prompt if password is not supplied)
  -w, --write-out="simple"                      set the output format (fields, json, protobuf, simple, table)
```

---

<!-- /Configuration Options -->
<div class="td-content">
<h1>Configuration options</h1>
<div class="lead">etcd configuration: files, flags, and environment variables</div>
<header class="article-meta">
</header>
<p>etcd is configurable through a configuration file, various command-line flags, and environment variables.</p>
<p>A reusable configuration file is a YAML file made with name and value of one or more command-line flags described below. In order to use this file, specify the file path as a value to the <code>--config-file</code> flag or <code>ETCD_CONFIG_FILE</code> environment variable. The <a href="https://github.com/etcd-io/etcd/blob/release-3.4/etcd.conf.yml.sample" target="_blank" rel="noopener">sample configuration file</a> can be used as a starting point to create a new configuration file as needed.</p>
<p>Options set on the command line take precedence over those from the environment. If a configuration file is provided, other command line flags and environment variables will be ignored.
For example, <code>etcd --config-file etcd.conf.yml.sample --data-dir /tmp</code> will ignore the <code>--data-dir</code> flag.</p>
<p>The format of environment variable for flag <code>--my-flag</code> is <code>ETCD_MY_FLAG</code>. It applies to all flags.</p>
<p>The <a href="http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.txt" target="_blank" rel="noopener">official etcd ports</a> are 2379 for client requests and 2380 for peer communication. The etcd ports can be set to accept TLS traffic, non-TLS traffic, or both TLS and non-TLS traffic.</p>
<p>To start etcd automatically using custom settings at startup in Linux, using a <a href="http://freedesktop.org/wiki/Software/systemd/" target="_blank" rel="noopener">systemd</a> unit is highly recommended.</p>
<p>The list of flags provided below may not be up-to-date due to ongoing development changes. For the latest available flags, run <code>etcd --help</code> or refer to the <a href="https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go" target="_blank" rel="noopener">etcd help</a>.</p>
<h2 id="member-flags">Member flags<a aria-hidden="true" href="#member-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<h3 id="--name">–name<a aria-hidden="true" href="#--name" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Human-readable name for this member.</li>
<li>default: “default”</li>
<li>env variable: ETCD_NAME</li>
<li>This value is referenced as this node’s own entries listed in the <code>--initial-cluster</code> flag (e.g., <code>default=http://localhost:2380</code>). This needs to match the key used in the flag if using <a href="../clustering/#static">static bootstrapping</a>. When using discovery, each member must have a unique name. <code>Hostname</code> or <code>machine-id</code> can be a good choice.</li>
</ul>
<h3 id="--data-dir">–data-dir<a aria-hidden="true" href="#--data-dir" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the data directory.</li>
<li>default: “${name}.etcd”</li>
<li>env variable: ETCD_DATA_DIR</li>
</ul>
<h3 id="--wal-dir">–wal-dir<a aria-hidden="true" href="#--wal-dir" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the dedicated wal directory. If this flag is set, etcd will write the WAL files to the walDir rather than the dataDir. This allows a dedicated disk to be used, and helps avoid io competition between logging and other IO operations.</li>
<li>default: ""</li>
<li>env variable: ETCD_WAL_DIR</li>
</ul>
<h3 id="--snapshot-count">–snapshot-count<a aria-hidden="true" href="#--snapshot-count" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Number of committed transactions to trigger a snapshot to disk.</li>
<li>default: “100000”</li>
<li>env variable: ETCD_SNAPSHOT_COUNT</li>
</ul>
<h3 id="--heartbeat-interval">–heartbeat-interval<a aria-hidden="true" href="#--heartbeat-interval" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) of a heartbeat interval.</li>
<li>default: “100”</li>
<li>env variable: ETCD_HEARTBEAT_INTERVAL</li>
</ul>
<h3 id="--election-timeout">–election-timeout<a aria-hidden="true" href="#--election-timeout" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) for an election to timeout. See <a href="../../tuning/#time-parameters">Documentation/tuning.md</a> for details.</li>
<li>default: “1000”</li>
<li>env variable: ETCD_ELECTION_TIMEOUT</li>
</ul>
<h3 id="--initial-election-tick-advance">–initial-election-tick-advance<a aria-hidden="true" href="#--initial-election-tick-advance" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Whether to fast-forward initial election ticks on boot for faster election. When it is true, then local member fast-forwards election ticks to speed up “initial” leader election trigger. This benefits the case of larger election ticks. Disabling this would slow down initial bootstrap process for cross datacenter deployments. Make your own tradeoffs by configuring this flag at the cost of slow initial bootstrap.</li>
<li>default: true</li>
<li>env variable: ETCD_INITIAL_ELECTION_TICK_ADVANCE</li>
</ul>
<h3 id="--listen-peer-urls">–listen-peer-urls<a aria-hidden="true" href="#--listen-peer-urls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>List of URLs to listen on for peer traffic. This flag tells the etcd to accept incoming requests from its peers on the specified scheme://IP:port combinations. Scheme can be http or https. Alternatively, use <code>unix://&lt;file-path&gt;</code> or <code>unixs://&lt;file-path&gt;</code> for unix sockets. If 0.0.0.0 is specified as the IP, etcd listens to the given port on all interfaces. If an IP address is given as well as a port, etcd will listen on the given port and interface. Multiple URLs may be used to specify a number of addresses and ports to listen on. The etcd will respond to requests from any of the listed addresses and ports.</li>
<li>default: “http://localhost:2380”</li>
<li>env variable: ETCD_LISTEN_PEER_URLS</li>
<li>example: “http://10.0.0.1:2380”</li>
<li>invalid example: “<a href="http://example.com:2380" target="_blank" rel="noopener">http://example.com:2380</a>” (domain name is invalid for binding)</li>
</ul>
<h3 id="--listen-client-urls">–listen-client-urls<a aria-hidden="true" href="#--listen-client-urls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>List of URLs to listen on for client traffic. This flag tells the etcd to accept incoming requests from the clients on the specified scheme://IP:port combinations. Scheme can be either http or https. Alternatively, use <code>unix://&lt;file-path&gt;</code> or <code>unixs://&lt;file-path&gt;</code> for unix sockets. If 0.0.0.0 is specified as the IP, etcd listens to the given port on all interfaces. If an IP address is given as well as a port, etcd will listen on the given port and interface. Multiple URLs may be used to specify a number of addresses and ports to listen on. The etcd will respond to requests from any of the listed addresses and ports.</li>
<li>default: “http://localhost:2379”</li>
<li>env variable: ETCD_LISTEN_CLIENT_URLS</li>
<li>example: “http://10.0.0.1:2379”</li>
<li>invalid example: “<a href="http://example.com:2379" target="_blank" rel="noopener">http://example.com:2379</a>” (domain name is invalid for binding)</li>
</ul>
<h3 id="--max-snapshots">–max-snapshots<a aria-hidden="true" href="#--max-snapshots" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Maximum number of snapshot files to retain (0 is unlimited)</li>
<li>default: 5</li>
<li>env variable: ETCD_MAX_SNAPSHOTS</li>
<li>The default for users on Windows is unlimited, and manual purging down to 5 (or some preference for safety) is recommended.</li>
</ul>
<h3 id="--max-wals">–max-wals<a aria-hidden="true" href="#--max-wals" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Maximum number of wal files to retain (0 is unlimited)</li>
<li>default: 5</li>
<li>env variable: ETCD_MAX_WALS</li>
<li>The default for users on Windows is unlimited, and manual purging down to 5 (or some preference for safety) is recommended.</li>
</ul>
<h3 id="--cors">–cors<a aria-hidden="true" href="#--cors" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Comma-separated white list of origins for CORS (cross-origin resource sharing).</li>
<li>default: ""</li>
<li>env variable: ETCD_CORS</li>
</ul>
<h3 id="--quota-backend-bytes">–quota-backend-bytes<a aria-hidden="true" href="#--quota-backend-bytes" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Raise alarms when backend size exceeds the given quota (0 defaults to low space quota).</li>
<li>default: 0</li>
<li>env variable: ETCD_QUOTA_BACKEND_BYTES</li>
</ul>
<h3 id="--backend-batch-limit">–backend-batch-limit<a aria-hidden="true" href="#--backend-batch-limit" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>BackendBatchLimit is the maximum operations before commit the backend transaction.</li>
<li>default: 0</li>
<li>env variable: ETCD_BACKEND_BATCH_LIMIT</li>
</ul>
<h3 id="--backend-bbolt-freelist-type">–backend-bbolt-freelist-type<a aria-hidden="true" href="#--backend-bbolt-freelist-type" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>The freelist type that etcd backend(bboltdb) uses (array and map are supported types).</li>
<li>default: map</li>
<li>env variable: ETCD_BACKEND_BBOLT_FREELIST_TYPE</li>
</ul>
<h3 id="--backend-batch-interval">–backend-batch-interval<a aria-hidden="true" href="#--backend-batch-interval" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>BackendBatchInterval is the maximum time before commit the backend transaction.</li>
<li>default: 0</li>
<li>env variable: ETCD_BACKEND_BATCH_INTERVAL</li>
</ul>
<h3 id="--max-txn-ops">–max-txn-ops<a aria-hidden="true" href="#--max-txn-ops" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Maximum number of operations permitted in a transaction.</li>
<li>default: 128</li>
<li>env variable: ETCD_MAX_TXN_OPS</li>
</ul>
<h3 id="--max-request-bytes">–max-request-bytes<a aria-hidden="true" href="#--max-request-bytes" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Maximum client request size in bytes the server will accept.</li>
<li>default: 1572864</li>
<li>env variable: ETCD_MAX_REQUEST_BYTES</li>
</ul>
<h3 id="--grpc-keepalive-min-time">–grpc-keepalive-min-time<a aria-hidden="true" href="#--grpc-keepalive-min-time" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Minimum duration interval that a client should wait before pinging server.</li>
<li>default: 5s</li>
<li>env variable: ETCD_GRPC_KEEPALIVE_MIN_TIME</li>
</ul>
<h3 id="--grpc-keepalive-interval">–grpc-keepalive-interval<a aria-hidden="true" href="#--grpc-keepalive-interval" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Frequency duration of server-to-client ping to check if a connection is alive (0 to disable).</li>
<li>default: 2h</li>
<li>env variable: ETCD_GRPC_KEEPALIVE_INTERVAL</li>
</ul>
<h3 id="--grpc-keepalive-timeout">–grpc-keepalive-timeout<a aria-hidden="true" href="#--grpc-keepalive-timeout" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Additional duration of wait before closing a non-responsive connection (0 to disable).</li>
<li>default: 20s</li>
<li>env variable: ETCD_GRPC_KEEPALIVE_TIMEOUT</li>
</ul>
<h2 id="clustering-flags">Clustering flags<a aria-hidden="true" href="#clustering-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<p><code>--initial-advertise-peer-urls</code>, <code>--initial-cluster</code>, <code>--initial-cluster-state</code>, and <code>--initial-cluster-token</code> flags are used in bootstrapping (<a href="../clustering/#static">static bootstrap</a>, <a href="../clustering/#discovery">discovery-service bootstrap</a> or <a href="../runtime-configuration/">runtime reconfiguration</a>) a new member, and ignored when restarting an existing member.</p>
<p><code>--discovery</code> prefix flags need to be set when using <a href="../clustering/#discovery">discovery service</a>.</p>
<h3 id="--initial-advertise-peer-urls">–initial-advertise-peer-urls<a aria-hidden="true" href="#--initial-advertise-peer-urls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>List of this member’s peer URLs to advertise to the rest of the cluster. These addresses are used for communicating etcd data around the cluster. At least one must be routable to all cluster members. These URLs can contain domain names.</li>
<li>default: “http://localhost:2380”</li>
<li>env variable: ETCD_INITIAL_ADVERTISE_PEER_URLS</li>
<li>example: “<a href="http://example.com:2380" target="_blank" rel="noopener">http://example.com:2380</a>, http://10.0.0.1:2380”</li>
</ul>
<h3 id="--initial-cluster">–initial-cluster<a aria-hidden="true" href="#--initial-cluster" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Initial cluster configuration for bootstrapping.</li>
<li>default: “default=http://localhost:2380”</li>
<li>env variable: ETCD_INITIAL_CLUSTER</li>
<li>The key is the value of the <code>--name</code> flag for each node provided. The default uses <code>default</code> for the key because this is the default for the <code>--name</code> flag.</li>
</ul>
<h3 id="--initial-cluster-state">–initial-cluster-state<a aria-hidden="true" href="#--initial-cluster-state" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Initial cluster state (“new” or “existing”). Set to <code>new</code> for all members present during initial static or DNS bootstrapping. If this option is set to <code>existing</code>, etcd will attempt to join the existing cluster. If the wrong value is set, etcd will attempt to start but fail safely.</li>
<li>default: “new”</li>
<li>env variable: ETCD_INITIAL_CLUSTER_STATE</li>
</ul>
<h3 id="--initial-cluster-token">–initial-cluster-token<a aria-hidden="true" href="#--initial-cluster-token" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Initial cluster token for the etcd cluster during bootstrap.</li>
<li>default: “etcd-cluster”</li>
<li>env variable: ETCD_INITIAL_CLUSTER_TOKEN</li>
</ul>
<h3 id="--advertise-client-urls">–advertise-client-urls<a aria-hidden="true" href="#--advertise-client-urls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>List of this member’s client URLs to advertise to the rest of the cluster. These URLs can contain domain names.</li>
<li>default: “http://localhost:2379”</li>
<li>env variable: ETCD_ADVERTISE_CLIENT_URLS</li>
<li>example: “<a href="http://example.com:2379" target="_blank" rel="noopener">http://example.com:2379</a>, http://10.0.0.1:2379”</li>
<li>Be careful if advertising URLs such as http://localhost:2379 from a cluster member and are using the proxy feature of etcd. This will cause loops, because the proxy will be forwarding requests to itself until its resources (memory, file descriptors) are eventually depleted.</li>
</ul>
<h3 id="--discovery">–discovery<a aria-hidden="true" href="#--discovery" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Discovery URL used to bootstrap the cluster.</li>
<li>default: ""</li>
<li>env variable: ETCD_DISCOVERY</li>
</ul>
<h3 id="--discovery-srv">–discovery-srv<a aria-hidden="true" href="#--discovery-srv" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>DNS srv domain used to bootstrap the cluster.</li>
<li>default: ""</li>
<li>env variable: ETCD_DISCOVERY_SRV</li>
</ul>
<h3 id="--discovery-srv-name">–discovery-srv-name<a aria-hidden="true" href="#--discovery-srv-name" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Suffix to the DNS srv name queried when bootstrapping using DNS.</li>
<li>default: ""</li>
<li>env variable: ETCD_DISCOVERY_SRV_NAME</li>
</ul>
<h3 id="--discovery-fallback">–discovery-fallback<a aria-hidden="true" href="#--discovery-fallback" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Expected behavior (“exit” or “proxy”) when discovery services fails. “proxy” supports v2 API only.</li>
<li>default: “proxy”</li>
<li>env variable: ETCD_DISCOVERY_FALLBACK</li>
</ul>
<h3 id="--discovery-proxy">–discovery-proxy<a aria-hidden="true" href="#--discovery-proxy" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>HTTP proxy to use for traffic to discovery service.</li>
<li>default: ""</li>
<li>env variable: ETCD_DISCOVERY_PROXY</li>
</ul>
<h3 id="--strict-reconfig-check">–strict-reconfig-check<a aria-hidden="true" href="#--strict-reconfig-check" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Reject reconfiguration requests that would cause quorum loss.</li>
<li>default: true</li>
<li>env variable: ETCD_STRICT_RECONFIG_CHECK</li>
</ul>
<h3 id="--auto-compaction-retention">–auto-compaction-retention<a aria-hidden="true" href="#--auto-compaction-retention" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Auto compaction retention for mvcc key value store in hour. 0 means disable auto compaction.</li>
<li>default: 0</li>
<li>env variable: ETCD_AUTO_COMPACTION_RETENTION</li>
</ul>
<h3 id="--auto-compaction-mode">–auto-compaction-mode<a aria-hidden="true" href="#--auto-compaction-mode" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Interpret ‘auto-compaction-retention’ one of: ‘periodic’, ‘revision’. ‘periodic’ for duration based retention, defaulting to hours if no time unit is provided (e.g. ‘5m’). ‘revision’ for revision number based retention.</li>
<li>default: periodic</li>
<li>env variable: ETCD_AUTO_COMPACTION_MODE</li>
</ul>
<h3 id="--enable-v2">–enable-v2<a aria-hidden="true" href="#--enable-v2" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Accept etcd V2 client requests</li>
<li>default: false</li>
<li>env variable: ETCD_ENABLE_V2</li>
</ul>
<h2 id="proxy-flags">Proxy flags<a aria-hidden="true" href="#proxy-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<p><code>--proxy</code> prefix flags configures etcd to run in <a href="/docs/v2.3/proxy/">proxy mode</a>. “proxy” supports v2 API only.</p>
<h3 id="--proxy">–proxy<a aria-hidden="true" href="#--proxy" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Proxy mode setting (“off”, “readonly” or “on”).</li>
<li>default: “off”</li>
<li>env variable: ETCD_PROXY</li>
</ul>
<h3 id="--proxy-failure-wait">–proxy-failure-wait<a aria-hidden="true" href="#--proxy-failure-wait" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) an endpoint will be held in a failed state before being reconsidered for proxied requests.</li>
<li>default: 5000</li>
<li>env variable: ETCD_PROXY_FAILURE_WAIT</li>
</ul>
<h3 id="--proxy-refresh-interval">–proxy-refresh-interval<a aria-hidden="true" href="#--proxy-refresh-interval" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) of the endpoints refresh interval.</li>
<li>default: 30000</li>
<li>env variable: ETCD_PROXY_REFRESH_INTERVAL</li>
</ul>
<h3 id="--proxy-dial-timeout">–proxy-dial-timeout<a aria-hidden="true" href="#--proxy-dial-timeout" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) for a dial to timeout or 0 to disable the timeout</li>
<li>default: 1000</li>
<li>env variable: ETCD_PROXY_DIAL_TIMEOUT</li>
</ul>
<h3 id="--proxy-write-timeout">–proxy-write-timeout<a aria-hidden="true" href="#--proxy-write-timeout" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) for a write to timeout or 0 to disable the timeout.</li>
<li>default: 5000</li>
<li>env variable: ETCD_PROXY_WRITE_TIMEOUT</li>
</ul>
<h3 id="--proxy-read-timeout">–proxy-read-timeout<a aria-hidden="true" href="#--proxy-read-timeout" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Time (in milliseconds) for a read to timeout or 0 to disable the timeout.</li>
<li>Don’t change this value if using watches because use long polling requests.</li>
<li>default: 0</li>
<li>env variable: ETCD_PROXY_READ_TIMEOUT</li>
</ul>
<h2 id="security-flags">Security flags<a aria-hidden="true" href="#security-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<p>The security flags help to <a href="../security/">build a secure etcd cluster</a>.</p>
<h3 id="--ca-file">–ca-file<a aria-hidden="true" href="#--ca-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<p><strong>DEPRECATED</strong></p>
<ul>
<li>Path to the client server TLS CA file. <code>--ca-file ca.crt</code> could be replaced by <code>--trusted-ca-file ca.crt --client-cert-auth</code> and etcd will perform the same.</li>
<li>default: ""</li>
<li>env variable: ETCD_CA_FILE</li>
</ul>
<h3 id="--cert-file">–cert-file<a aria-hidden="true" href="#--cert-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the client server TLS cert file.</li>
<li>default: ""</li>
<li>env variable: ETCD_CERT_FILE</li>
</ul>
<h3 id="--key-file">–key-file<a aria-hidden="true" href="#--key-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the client server TLS key file.</li>
<li>default: ""</li>
<li>env variable: ETCD_KEY_FILE</li>
</ul>
<h3 id="--client-cert-auth">–client-cert-auth<a aria-hidden="true" href="#--client-cert-auth" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Enable client cert authentication.</li>
<li>default: false</li>
<li>env variable: ETCD_CLIENT_CERT_AUTH</li>
<li>CN authentication is not supported by gRPC-gateway.</li>
</ul>
<h3 id="--client-crl-file">–client-crl-file<a aria-hidden="true" href="#--client-crl-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the client certificate revocation list file.</li>
<li>default: ""</li>
<li>env variable: ETCD_CLIENT_CRL_FILE</li>
</ul>
<h3 id="--client-cert-allowed-hostname">–client-cert-allowed-hostname<a aria-hidden="true" href="#--client-cert-allowed-hostname" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Allowed Allowed TLS name for client cert authentication.</li>
<li>default: ""</li>
<li>env variable: ETCD_CLIENT_CERT_ALLOWED_HOSTNAME</li>
</ul>
<h3 id="--trusted-ca-file">–trusted-ca-file<a aria-hidden="true" href="#--trusted-ca-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the client server TLS trusted CA cert file.</li>
<li>default: ""</li>
<li>env variable: ETCD_TRUSTED_CA_FILE</li>
</ul>
<h3 id="--auto-tls">–auto-tls<a aria-hidden="true" href="#--auto-tls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Client TLS using generated certificates</li>
<li>default: false</li>
<li>env variable: ETCD_AUTO_TLS</li>
</ul>
<h3 id="--peer-ca-file">–peer-ca-file<a aria-hidden="true" href="#--peer-ca-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<p><strong>DEPRECATED</strong></p>
<ul>
<li>Path to the peer server TLS CA file. <code>--peer-ca-file ca.crt</code> could be replaced by <code>--peer-trusted-ca-file ca.crt --peer-client-cert-auth</code> and etcd will perform the same.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_CA_FILE</li>
</ul>
<h3 id="--peer-cert-file">–peer-cert-file<a aria-hidden="true" href="#--peer-cert-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the peer server TLS cert file. This is the cert for peer-to-peer traffic, used both for server and client.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_CERT_FILE</li>
</ul>
<h3 id="--peer-key-file">–peer-key-file<a aria-hidden="true" href="#--peer-key-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the peer server TLS key file. This is the key for peer-to-peer traffic, used both for server and client.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_KEY_FILE</li>
</ul>
<h3 id="--peer-client-cert-auth">–peer-client-cert-auth<a aria-hidden="true" href="#--peer-client-cert-auth" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Enable peer client cert authentication.</li>
<li>default: false</li>
<li>env variable: ETCD_PEER_CLIENT_CERT_AUTH</li>
</ul>
<h3 id="--peer-crl-file">–peer-crl-file<a aria-hidden="true" href="#--peer-crl-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the peer certificate revocation list file.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_CRL_FILE</li>
</ul>
<h3 id="--peer-trusted-ca-file">–peer-trusted-ca-file<a aria-hidden="true" href="#--peer-trusted-ca-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Path to the peer server TLS trusted CA file.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_TRUSTED_CA_FILE</li>
</ul>
<h3 id="--peer-auto-tls">–peer-auto-tls<a aria-hidden="true" href="#--peer-auto-tls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Peer TLS using generated certificates</li>
<li>default: false</li>
<li>env variable: ETCD_PEER_AUTO_TLS</li>
</ul>
<h3 id="--peer-cert-allowed-cn">–peer-cert-allowed-cn<a aria-hidden="true" href="#--peer-cert-allowed-cn" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Allowed CommonName for inter peer authentication.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_CERT_ALLOWED_CN</li>
</ul>
<h3 id="--peer-cert-allowed-hostname">–peer-cert-allowed-hostname<a aria-hidden="true" href="#--peer-cert-allowed-hostname" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Allowed TLS certificate name for inter peer authentication.</li>
<li>default: ""</li>
<li>env variable: ETCD_PEER_CERT_ALLOWED_HOSTNAME</li>
</ul>
<h3 id="--cipher-suites">–cipher-suites<a aria-hidden="true" href="#--cipher-suites" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Comma-separated list of supported TLS cipher suites between server/client and peers.</li>
<li>default: ""</li>
<li>env variable: ETCD_CIPHER_SUITES</li>
</ul>
<h3 id="--tls-min-version">–tls-min-version<a aria-hidden="true" href="#--tls-min-version" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Minimum TLS version supported by etcd.</li>
<li>default: “TLS1.2”</li>
</ul>
<h3 id="--tls-max-version">–tls-max-version<a aria-hidden="true" href="#--tls-max-version" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Maximum TLS version supported by etcd.</li>
<li>detault: ""</li>
</ul>
<h2 id="logging-flags">Logging flags<a aria-hidden="true" href="#logging-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<h3 id="--logger">–logger<a aria-hidden="true" href="#--logger" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<p><strong>Available from v3.4.</strong>
<strong>WARNING: <code>--logger=capnslog</code> to be deprecated in v3.5.</strong></p>
<ul>
<li>Specify ‘zap’ for structured logging or ‘capnslog’.</li>
<li>default: capnslog</li>
<li>env variable: ETCD_LOGGER</li>
</ul>
<h3 id="--log-outputs">–log-outputs<a aria-hidden="true" href="#--log-outputs" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Specify ‘stdout’ or ‘stderr’ to skip journald logging even when running under systemd, or list of comma separated output targets.</li>
<li>default: default</li>
<li>env variable: ETCD_LOG_OUTPUTS</li>
<li>‘default’ use ‘stderr’ config for v3.4 during zap logger migraion</li>
</ul>
<h3 id="--log-level">–log-level<a aria-hidden="true" href="#--log-level" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<p><strong>Available from v3.4.</strong></p>
<ul>
<li>Configures log level. Only supports debug, info, warn, error, panic, or fatal.</li>
<li>default: info</li>
<li>env variable: ETCD_LOG_LEVEL</li>
<li>‘default’ use ‘info’.</li>
</ul>
<h3 id="--debug">–debug<a aria-hidden="true" href="#--debug" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<p><strong>WARNING: to be deprecated in v3.5.</strong></p>
<ul>
<li>Drop the default log level to DEBUG for all subpackages.</li>
<li>default: false (INFO for all packages)</li>
<li>env variable: ETCD_DEBUG</li>
</ul>
<h3 id="--log-package-levels">–log-package-levels<a aria-hidden="true" href="#--log-package-levels" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<p><strong>WARNING: to be deprecated in v3.5.</strong></p>
<ul>
<li>Set individual etcd subpackages to specific log levels. An example being <code>etcdserver=WARNING,security=DEBUG</code></li>
<li>default: "" (INFO for all packages)</li>
<li>env variable: ETCD_LOG_PACKAGE_LEVELS</li>
</ul>
<h2 id="unsafe-flags">Unsafe flags<a aria-hidden="true" href="#unsafe-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<p>Please be CAUTIOUS when using unsafe flags because it will break the guarantees given by the consensus protocol.
For example, it may panic if other members in the cluster are still alive.
Follow the instructions when using these flags.</p>
<h3 id="--force-new-cluster">–force-new-cluster<a aria-hidden="true" href="#--force-new-cluster" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Force to create a new one-member cluster. It commits configuration changes forcing to remove all existing members in the cluster and add itself, but is strongly discouraged. Please review the <a href="../recovery/">disaster recovery</a> documentation for preferred v3 recovery procedures.</li>
<li>default: false</li>
<li>env variable: ETCD_FORCE_NEW_CLUSTER</li>
</ul>
<h2 id="miscellaneous-flags">Miscellaneous flags<a aria-hidden="true" href="#miscellaneous-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<h3 id="--version">–version<a aria-hidden="true" href="#--version" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Print the version and exit.</li>
<li>default: false</li>
</ul>
<h3 id="--config-file">–config-file<a aria-hidden="true" href="#--config-file" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Load server configuration from a file. Note that if a configuration file is provided, other command line flags and environment variables will be ignored.</li>
<li>default: ""</li>
<li>example: <a href="https://github.com/etcd-io/etcd/blob/release-3.4/etcd.conf.yml.sample" target="_blank" rel="noopener">sample configuration file</a></li>
<li>env variable: ETCD_CONFIG_FILE</li>
</ul>
<h2 id="profiling-flags">Profiling flags<a aria-hidden="true" href="#profiling-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<h3 id="--enable-pprof">–enable-pprof<a aria-hidden="true" href="#--enable-pprof" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Enable runtime profiling data via HTTP server. Address is at client URL + “/debug/pprof/”</li>
<li>default: false</li>
<li>env variable: ETCD_ENABLE_PPROF</li>
</ul>
<h3 id="--metrics">–metrics<a aria-hidden="true" href="#--metrics" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Set level of detail for exported metrics, specify ‘extensive’ to include server side grpc histogram metrics.</li>
<li>default: basic</li>
<li>env variable: ETCD_METRICS</li>
</ul>
<h3 id="--listen-metrics-urls">–listen-metrics-urls<a aria-hidden="true" href="#--listen-metrics-urls" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>List of additional URLs to listen on that will respond to both the <code>/metrics</code> and <code>/health</code> endpoints</li>
<li>default: ""</li>
<li>env variable: ETCD_LISTEN_METRICS_URLS</li>
</ul>
<h2 id="auth-flags">Auth flags<a aria-hidden="true" href="#auth-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<h3 id="--auth-token">–auth-token<a aria-hidden="true" href="#--auth-token" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Specify a token type and token specific options, especially for JWT. Its format is “type,var1=val1,var2=val2,…”. Possible type is ‘simple’ or ‘jwt’. Possible variables are ‘sign-method’ for specifying a sign method of jwt (its possible values are ‘ES256’, ‘ES384’, ‘ES512’, ‘HS256’, ‘HS384’, ‘HS512’, ‘RS256’, ‘RS384’, ‘RS512’, ‘PS256’, ‘PS384’, or ‘PS512’), ‘pub-key’ for specifying a path to a public key for verifying jwt, ‘priv-key’ for specifying a path to a private key for signing jwt, and ‘ttl’ for specifying TTL of jwt tokens.</li>
<li>For asymmetric algorithms (‘RS’, ‘PS’, ‘ES’), the public key is optional, as the private key contains enough information to both sign and verify tokens.</li>
<li>Example option of JWT: ‘–auth-token jwt,pub-key=app.rsa.pub,priv-key=app.rsa,sign-method=RS512,ttl=10m’</li>
<li>default: “simple”</li>
<li>env variable: ETCD_AUTH_TOKEN</li>
</ul>
<h3 id="--bcrypt-cost">–bcrypt-cost<a aria-hidden="true" href="#--bcrypt-cost" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Specify the cost / strength of the bcrypt algorithm for hashing auth passwords. Valid values are between 4 and 31.</li>
<li>default: 10</li>
<li>env variable: (not supported)</li>
</ul>
<h2 id="experimental-flags">Experimental flags<a aria-hidden="true" href="#experimental-flags" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h2>
<h3 id="--experimental-corrupt-check-time">–experimental-corrupt-check-time<a aria-hidden="true" href="#--experimental-corrupt-check-time" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Duration of time between cluster corruption check passes</li>
<li>default: 0s</li>
<li>env variable: ETCD_EXPERIMENTAL_CORRUPT_CHECK_TIME</li>
</ul>
<h3 id="--experimental-compaction-batch-limit">–experimental-compaction-batch-limit<a aria-hidden="true" href="#--experimental-compaction-batch-limit" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>Sets the maximum revisions deleted in each compaction batch.</li>
<li>default: 1000</li>
<li>env variable: ETCD_EXPERIMENTAL_COMPACTION_BATCH_LIMIT</li>
</ul>
<h3 id="--experimental-peer-skip-client-san-verification">–experimental-peer-skip-client-san-verification<a aria-hidden="true" href="#--experimental-peer-skip-client-san-verification" style="visibility: hidden;"> <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></a></h3>
<ul>
<li>
<p>Skip verification of SAN field in client certificate for peer connections. This can be helpful e.g. if
cluster members run in different networks behind a NAT.</p>
<p>In this case make sure to use peer certificates based on
a private certificate authority using <code>--peer-cert-file</code>, <code>--peer-key-file</code>, <code>--peer-trusted-ca-file</code></p>
</li>
<li>
<p>default: false</p>
</li>
<li>
<p>env variable: ETCD_EXPERIMENTAL_PEER_SKIP_CLIENT_SAN_VERIFICATION</p>
</li>
</ul>
<style>.feedback--answer{display:inline-block}.feedback--answer-no{margin-left:1em}.feedback--response{display:none;margin-top:1em}.feedback--response__visible{display:block}</style>
<div class="d-print-none">
<h2 class="feedback--title">Feedback</h2>
<p class="feedback--question">Was this page helpful?</p>
<button class="btn btn-primary mb-4 feedback--answer feedback--answer-yes">Yes</button>
<button class="btn btn-primary mb-4 feedback--answer feedback--answer-no">No</button>
<p class="feedback--response feedback--response-yes">
Glad to hear it! Please <a href="https://github.com/etcd-io/website/issues/new">tell us how we can improve</a>.
</p>
<p class="feedback--response feedback--response-no">
Sorry to hear that. Please <a href="https://github.com/etcd-io/website/issues/new">tell us how we can improve</a>.
</p>
</div>
<script>const yesButton=document.querySelector('.feedback--answer-yes'),noButton=document.querySelector('.feedback--answer-no'),yesResponse=document.querySelector('.feedback--response-yes'),noResponse=document.querySelector('.feedback--response-no'),disableButtons=()=>{yesButton.disabled=!0,noButton.disabled=!0},sendFeedback=b=>{if(typeof ga!='function')return;const a={command:'send',hitType:'event',category:'Helpful',action:'click',label:window.location.pathname,value:b};ga(a.command,a.hitType,a.category,a.action,a.label,a.value)};yesButton.addEventListener('click',()=>{yesResponse.classList.add('feedback--response__visible'),disableButtons(),sendFeedback(1)}),noButton.addEventListener('click',()=>{noResponse.classList.add('feedback--response__visible'),disableButtons(),sendFeedback(0)})</script>
<br>
<div class="text-muted mt-5 pt-3 border-top">
Last modified March 16, 2023: <a href="https://github.com/etcd-io/website/commit/2bd8cb23c4adc5309a2ea62534f6a4cc1e9bc569">Update 3.4 op-guide to document tls min/max options. (2bd8cb2)</a>
</div>
</div>