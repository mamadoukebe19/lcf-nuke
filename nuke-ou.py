import boto3
import os
import subprocess

def get_ous_accounts(parent_ou_id: str) -> list[dict]:
    """
    Get all accounts under an OU
    :param parent_ou_id:
    :return:
    """
    client = boto3.client("organizations", region_name="us-east-1")
    accounts = []
    response = client.list_children(
        ParentId=parent_ou_id, ChildType="ACCOUNT", MaxResults=20
    )

    while True:
        accounts += response["Children"]
        if "NextToken" in response:
            response = client.list_children(
                ParentId=parent_ou_id,
                ChildType="ACCOUNT",
                MaxResults=20,
                NextToken=response["NextToken"],
            )
        else:
            break

    for acc in accounts:
        acc["Detail"] = client.describe_account(AccountId=acc["Id"])["Account"]
    return response["Children"]

def assume_role(account_id: str, role_name: str) -> dict:
    """
    Assume a role in an account
    :param account_id:
    :param role_name:
    :return:
    """
    client = boto3.client("sts")
    response = client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName="nuke-ou",
    )
    return response["Credentials"]


if __name__ == "__main__":
    ou_id = os.environ["PARENT_OU_ID"]
    role_name = os.environ["ROLE_NAME"]

    ou_accounts = get_ous_accounts(ou_id)

    for account in ou_accounts:
        account_id = account["Id"]
        print(f"Nuking the account {account['Id']}/{account['Detail']['Name']}")
        cmd = ["aws-nuke", "nuke", "-c", "nuke-config.yml", "--assume-role-arn", f"arn:aws:iam::{account_id}:role/{role_name}"]
        completed_process = subprocess.run(cmd, check=True)


