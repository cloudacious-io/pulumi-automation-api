export PATH=$PATH:/root/.pulumi/bin

function webhook() {
    python iac/webhook.py
}
