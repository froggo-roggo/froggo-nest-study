## Hi there 👋

### Intro
NEST를 공부해보기 위해 만든 페이지

NEST: 신경세포들의 정확한 형태보다는, 신경계의 시스템적인 동작, 규모, 구조에 초점을 맞춘 스파이킹 신경망 모델 시뮬레이터이다. NEST의 개발은 NEST 이니셔티브(Nest Initiative)에서 주도적으로 이뤄지고 있다.

NEST 이니셔티브 관련 정보: <a href = "https://www.nest-initiative.org">링크 </a>

### NEST 사용법
* 수동 다운로드: <a href = "https://www.nest-simulator.org/download/">다운로드 링크</a>에서 환경에 맞는 버전의 nest를 다운로드 받는다.
** git bash를 설치한 후 로컬 터미널에서 git clone https://github.com/nest/nest-simulator.git 커맨드로 쉽게 다운로드 받을 수 있다. (github에 올라온 것이 최신 버전인지 한 번 확인하고 다운)
** 이론상 cmake CMakeLists.txt를 실행하면 사용 가능해야 한다... (그러나 실제로는 수많은 패키지 의존성 문제에 직면할 것)

* 리눅스 환경 설치: <a href="https://nest-simulator.readthedocs.io/en/stable/installation/user.html#user-install">참조</a>
** 따라서 리눅스를 쓰는 편이 이후의 과정에서 마음 편하다
** windows에서 bash를 켜면 linux/unix에서와 똑같이 진행 가능

2. 파이썬 API 사용 준비
* 리눅스: source /bin/nest_vars.sh 실행
** 이때 설치 경로는 nest-simulator가 실제 깔려 있는 경로에 따라 달라진다.
* 환경변수 제대로 설정됐는지 확인하는 법 
** 리눅스: echo ${[변수명]}
** 윈도우 Powershell: $Env:[변수명]
** 정상적으로 설치가 되었다면, 아무 파이썬이나 켜서 (버전 3.8 이상) 인터프리터 상에서 import nest를 했을 때 NEST 설명 document가 뜬다.

3. 참조: <a href = "https://nest-simulator.readthedocs.io/en/stable/">NEST 튜토리얼 페이지</a>
<a href = "https://nest-simulator.readthedocs.io/en/stable/examples/index.html#pynest-examples">PyNEST 예제 페이지</a>






