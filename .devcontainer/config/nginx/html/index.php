<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
        }
        header {
            background-color: #666;
            padding: 30px;
            text-align: center;
            font-size: 35px;
            color: white;
        }
        /* center main */
        main {
            max-width: 80%;
            margin: 0 auto;
            padding: 0 20px;
            align-items: center;

        }
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }
        li a {
            display: block;
            color: #000;
            padding: 8px 16px;
            text-decoration: none;
        }
        li a:hover {
            background-color: #555;
            color: white;
        }
    </style>
    <title>Proxy Service</title>
</head>
<body>
    <header>
    <h1>Proxy Service</h1>
    </header>
    <main>

        <p>Proxy Service is running on <strong><?php echo gethostname(); ?></strong></p>
        <p>Services available:</p>
        <!-- Services include: etcd, milvus, mysql, nginx, proxy, redis, zookeeper  -->
        <ul>
            <li><a href="http://127.0.0.1:2379">etcd</a> <span id="etcd-cluster"></span></li>
            <li><a href="http://127.0.0.1:19530">milvus</a> <span id="milvus-service"></span></li>
            <!--      Make http request to milvus health check endpoint and return the result.   -->
            <li><a href="http://127.0.0.1:9091/api/v1/health">milvus-health</a> <span id="milvus-health-check"></span></li>
            <li><a href="http://127.0.0.1:3306">mysql</a> <span id="mysql-service"></span></li>
            <li><a href="http://127.0.0.1:8080">nginx proxy</a> <span id="nginx-proxy"></span></li>
        </ul>
    </main>
    <script>
        const endpoints = {
        "etcd-cluster": "http://127.0.0.1:2379/v3/members",
        };
        const query_error = document.querySelector(".query-error");
        const mutation_error = document.querySelector(".mutation-error");
        /**
         * Query function that sends query object to the server
         * @description Query
         * @returns {Promise<void>}
         */
        async function query(event) {
            event.preventDefault();
            const query = document.getElementById("query").value;
            //const error = document.querySelector(".query-error");
            try {
                if (!query) {
                    query_error.style.color = "red";
                    query_error.innerHTML = "Please enter a query!";
                    return;
                }
                query_error.innerHTML = "";
                const response = await axios.post(endpoints.query, {
                  query
                });
                const data = document.createElement("pre");
                data.innerHTML = JSON.stringify(response.data, null, 2);
                data.appendChild(document.createElement("hr"));
                document.getElementById("response").appendChild(data);
            } catch (error) {
                console.dir(error.response.data);
                const error_element = document.createElement("pre");
                error_element.style.color = "red";
                error_element.innerHTML = JSON.stringify(error.response.data.errors, null, 2);
                query_error.appendChild(error_element);
            }
        }

    </script>
</body>
</html>
