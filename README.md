# Realtime Sentiment Classification with FastAPI

** FastAPI 기반 Kubernetes 앱 배포를 바탕으로, GCP에 존재하는 ML 모델을 서빙하는 프로젝트입니다. **

모델 학습 및 아티팩트 배포와 관련된 소스 및 블로그 설명은 다음 링크를 참고해주시기 바랍니다.

[Code source](https://github.com/jihoahn9303/MLflow-with-GCP)

[Blog](https://anzzang-lab.oopy.io/55636845-9a23-455e-8234-8a41180615ff)


## Machine Learning Task

머신러닝 태스크의 경우, 영문 리뷰를 기반으로 한 이진 감성 분류 문제를 선택하였습니다. (positive/negative)

모델 학습 및 평가를 위한 데이터로서, Kaggle에서 제공한 'IMDB Dataset of 50K Movie Reviews'를 사용하였습니다.

자세한 내용은 [링크](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)를 참고해주세요 :)


## Project process

![serving project](https://github.com/jihoahn9303/fastapi-model-serving/assets/48744746/b8f2de3f-1e32-446b-9d6d-097a02f489dd)

1. 모델 서빙에 필요한 코드를 `Github`에 push할 경우, `Github Actions`을 통해 자동으로 코드를 컨테이너로 `build`합니다.

2. 빌드 된 컨테이너는 `GCP Artifact Registry`에 자동으로 배포됩니다.

3. `Github Actions`의 워크플로우에 의하여, 컨테이너는 `GCP Kubernetes`에 Kubernetes 애플리케이션 형태로 배포됩니다.

4. ArgoCD Server를 통해 Kubernetes 애플리케이션에 대한 `Health check`를 자동으로 수행합니다.

5. `Health check`가 완료된 애플리케이션은 `GCP Cloud SQL`에 쿼리를 수행하여, 성능이 가장 좋은 모델 URL을 가져옵니다.

6. `GCP Cloud Storage`에서 URL에 대응하는 모델을 가져옵니다.

7. FastAPI 웹 애플리케이션은 가져온 모델을 통해, 추론(inference)을 수행할 준비를 마칩니다.


## Project structure

본 프로젝트의 파일 구성요소는 다음과 같습니다.

```
.
├── Dockerfile
├── README.md
├── chart
│   ├── Chart.yaml
│   ├── charts
│   ├── sentiment-helm-0.0.1.tgz
│   ├── templates
│   │   ├── NOTES.txt
│   │   ├── _helpers.tpl
│   │   ├── deployment.yaml
│   │   ├── hpa.yaml
│   │   ├── ingress.yaml
│   │   ├── service.yaml
│   │   ├── serviceaccount.yaml
│   │   └── tests
│   │       └── test-connection.yaml
│   └── values.yaml
├── database
│   ├── __init__.py
│   ├── database_setting.py
│   └── model.py
├── main.py
├── nlp-mlops-service-account.json
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── scripts
│   └── create_env.sh
└── src
    ├── __init__.py
    └── model.py
```

## Develop & Experiment environment

개발 환경에 대한 주요 사항은 아래와 같습니다.

| Source                  | Version                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------- |
| OS(Host)                | Host: Microsoft Windows 10 Pro build `19045` / NVIDIA GeForce RTX 3060 12GB           |
| Remote controller       | WSL2 / Ubuntu version: `20.04`                                                        |
| Python                  | `3.9.10`                                                                              |
| IDLE                    | Visual Studio code `1.75.1`                                                           |
| Docker                  | Docker desktop `4.26.1` / Engine version: `24.0.7`                                    |



