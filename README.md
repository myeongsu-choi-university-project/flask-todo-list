## Todo 리스트 애플리케이션

### 환경 설정
- MySQL Server 설치 
- MySQL Query 입력 탭에서 다음 명령을 실행:

    ```SQL
    /* MySQL 서버에 새 데이터 베이스 생성 */
    CREATE DATABASE flask_todo_db;

    /* 새 MySQL 사용자를 생성하고 권한을 부여 */
    CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON flask_todo_db.* TO 'flask_user'@'localhost'; 
    FLUSH PRIVILEGES;
    ```

## 실행 방법
1. 가상환경 생성
    ```bash
    python -m venv venv
    ```
2. 가상환경 활성화
    ```bash
    venv\Scripts\activate
    ```
3. 의존성 설치
    ```bash
    pip install -r requirements.txt
    ```
4. 웹 시스템 실행
    ```bash
    python app.py
    ```
브라우저에서 http://localhost:5000으로 접속하여 시스템을 확인할 수 있다.

## 요구사항
- Todo 리스트 애플리케이션을 데이터베이스를 사용할 수 있도록 개선
- Todo 라우트들에 대응하는 프론트엔드 개발
- SQLAlchemy와 템플릿 문법을 활용하여 구현
---
- 데이터 추가: 폼 제출 시 새로운 Todo 객체를 생성하고 데이터베이스에 추가
- 데이터 조회: Todo.query.all()을 사용하여 모든 Todo 항목을 로드
- 데이터 수정: complete 라우트에서 Todo 항목의 완료 상태를 토글
- 데이터 수정: edit 라우트를 추가하여 Todo 항목의 제목과 설명을 수정할 수 있게 함
- 데이터 삭제: delete 라우트에서 db.session.delete()를 사용하여 항목을 삭제


## 결과 
![alt text](/images/image-1.png)

    