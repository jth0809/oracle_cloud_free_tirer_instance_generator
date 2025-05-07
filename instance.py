import oci
import time
from oci.exceptions import ServiceError


# 사용자 정의 입력
COMPARTMENT_ID = "YOUR_COMPARTMENT_ID"  # 당신의 컴파트먼트 OCID를 여기에 입력하세요
AVAILABILITY_DOMAIN = "YOUR_AD"  # 당신의 가용 영역을 여기에 입력하세요
SUBNET_ID = "YOUR_SUBNET_ID"  # 당신의 서브넷 OCID를 여기에 입력하세요
IMAGE_ID = "YOUR_IMAGE_ID"  # 당신의 이미지 OCID를 여기에 입력하세요
SHAPE = "VM.Standard.A1.Flex" # 인스턴스 컴퓨팅 종류 (ARM)
SSH_KEY_PATH = "~/.oci/oci_api_key_ssh.pub"  # 당신의 SSH 공개키 경로를 여기에 입력하세요

INSTANCE_NAME = "my-free-instance" #당신의 인스턴스 이름을 여기에 입력하세요
OCPU_COUNT = 4 # OCPU 수 (최대 4개)
MEMORY_GB = 24 # 메모리 크기 (최대 24GB)

MAX_RETRIES = 100000000 # 최대 재시도 횟수
RETRY_INTERVAL = 60  # 초 (1분)


def make_launch_details(ssh_key_str):
    return oci.core.models.LaunchInstanceDetails(
        compartment_id      = COMPARTMENT_ID,
        availability_domain = AVAILABILITY_DOMAIN,
        shape               = SHAPE,
        display_name        = INSTANCE_NAME,
        source_details      = oci.core.models.InstanceSourceViaImageDetails(
                                    source_type="image",
                                    image_id=IMAGE_ID
                              ),
        create_vnic_details = oci.core.models.CreateVnicDetails(
                                    subnet_id=SUBNET_ID,
                                    assign_public_ip=True
                              ),
        metadata            = {"ssh_authorized_keys": ssh_key_str},
        shape_config        = oci.core.models.LaunchInstanceShapeConfigDetails(
                                    ocpus=OCPU_COUNT,
                                    memory_in_gbs=MEMORY_GB
                              )
    )

def launch_with_retries():
    config        = oci.config.from_file()  # ~/.oci/config, DEFAULT
    compute_client= oci.core.ComputeClient(config)

    with open(SSH_KEY_PATH) as f:
        ssh_key = f.read().strip()

    details = make_launch_details(ssh_key)

    for attempt in range(1, MAX_RETRIES+1):
        print(f"[{attempt}/{MAX_RETRIES}] launching instance…")
        try:
            resp = compute_client.launch_instance(details)
            print("[SUCCESS] Instance OCID:", resp.data.id)
            return
        except ServiceError as e:
            if e.code == "OutOfHostCapacity" or "capacity" in e.message:
                print("[INFO] Host capacity full; retrying in", RETRY_INTERVAL, "seconds.")
                time.sleep(RETRY_INTERVAL)
                continue
            else:
                print("[FATAL] ServiceError:", e.code, e.message)
                break
        except Exception as e:
            print("[EXCEPTION]", str(e))
            break
    else:
        print("[ERROR] Reached max retries without success.")

if __name__ == "__main__":
    launch_with_retries()