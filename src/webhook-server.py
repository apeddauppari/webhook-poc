from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Define the PVC volume to be added
PVC_NAME = "minio-volume-minio-0"

@app.route("/mutate", methods=["POST"])
def mutate():
    request_data = request.get_json()
    print("Request data in webhook server:", request_data)
    try:
        # Extract pod spec
        pod = request_data["request"]["object"]
        namespace = request_data["request"]["namespace"]

        # Only mutate pods in "default"
        if namespace != "default":
            return jsonify({"response": {"allowed": True}})

        # Add a persistent volume if not already present
        patch = [
            {
                "op": "add",
                "path": "/spec/volumes/-",
                "value": {
                    "name": "local-pv-node0",
                    "persistentVolumeClaim": {"claimName": PVC_NAME}
                }
            },
            {
                "op": "add",
                "path": "/spec/containers/0/volumeMounts/-",
                "value": {
                    "mountPath": "/mnt/disk1/data",
                    "name": "local-pv-node0"
                }
            },
            {   "op": "add", 
                "path": "/metadata/labels/webhook-injected", 
                "value": "true"
            }
        ]

        response = {
            "response": {
                "uid": request_data["request"]["uid"],
                "allowed": True,
                "patchType": "JSONPatch",
                "patch": json.dumps(patch).encode("utf-8").decode("latin1")  # Base64 encode
            }
        }

        return jsonify(response)

    except Exception as e:
        print("Error in webhook server:", e)
        return jsonify({"response": {"allowed": False}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=("/certs/tls.crt", "/certs/tls.key"))

