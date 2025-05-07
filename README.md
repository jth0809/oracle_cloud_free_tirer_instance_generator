# oracle_cloud_free_tier_instance_generator

오라클 클라우드 프리 티어 인스턴스 생성기

---

## 배경
### 개발 이유
간단하게 정리된 한글 문서가 없는 것 같아 정리를 해봤습니다.

## 📦 사용 방법

### 🔧 설치

#### 1. Python 설치
Python 3.6 이상이 필요합니다.

#### 2. Python SDK 설치
```bash
pip install oci
```

#### 3. OCI CLI 설치
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

---

## ☁️ 오라클 클라우드 연동 절차

### 1. 인증정보 설정
OCI CLI 명령어를 통해 인증 설정을 진행합니다.
```bash
oci setup config
```

- 사용자 OCID
- 테넌시 OCID
- 리전
- 암호키 생성

### 2. OCID 확인
오라클 클라우드 → 사용자 설정 → **API KEYS** 메뉴에서 API Key 생성 후 OCID 확인

### 3. 공개키 등록
CLI에서 생성된 공개키(`~/.oci/oci_api_key_public.pem`)를 웹에 등록

1. 오라클 클라우드 계정 설정 → API KEYS
2. 공개키 등록
3. **적용까지 수 분 소요**

---

## ⚙️ `instance.py` 설정

### 1. SSH 키 변환
```bash
ssh-keygen -y -f ~/.oci/oci_api_key.pem > ~/.oci/oci_api_key_ssh.pub
```

### 2. 네트워크 요청 캡처
1. 오라클 클라우드 → 인스턴스 생성 페이지 (무료 인스턴스 설정)
2. 브라우저 F12 (개발자 모드) → Network 탭 → "instance" 검색
3. 오라클 클라우드 인스턴스 설정 후 생성 클릭 → 개발자 모드에서 instance 항목 우클릭 → `Copy as cURL (bash)`

### 3. 복사한 항목에서 메타데이터 안에 있는 다음 정보 추출
- `compartmentId`
- `availabilityDomain`
- `subnetId`
- `imageId`

### 4. `instance.py` 수정

```python
COMPARTMENT_ID = "ocid1.compartment.oc1..."
AVAILABILITY_DOMAIN = "kIdX:AP-CHUNCHEON-1-AD-1"
SUBNET_ID = "ocid1.subnet.oc1..."
IMAGE_ID = "ocid1.image.oc1..."
```

---

## 실행

```bash
python3 instance.py
```

스크립트는 인스턴스가 생성될 때까지 자동 재시도합니다.  
오류 코드 `OutOfHostCapacity` 를 감지하여 재시도합니다.
이외 에러는 에러 내용과 함께 종료.

---

