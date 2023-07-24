## 파트 1: 뉴런 및 간단한 신경 네트워크
- 원문: <a href="https://nest-simulator.readthedocs.io/en/stable/tutorials/pynest_tutorial/part_1_neurons_and_simple_neural_networks.html#pynest-tutorial-1">링크</a>
  - 안 중요한 내용은 적당히 뺐으니 정확한 내용은 반드시 원문을 참조

### 서론

### PyNEST - NEST 시뮬레이터 인터페이스

<img src ="https://nest-simulator.readthedocs.io/en/stable/_images/python_interface.png">
*Figure 1* 파이썬 인터페이스가 작동하는 방식. 파이썬 인터프리터가 nest 모듈을 인식하고 import하면, NEST Simulator kernel가 동적으로 로드된다. 사용자의 sim1ulation script에 쓰이는 function은 모두 이 high-level API에 정의되어 있으며 (즉, Python level), 이 함수들이 NEST의 기본 언어(시뮬레이션 언어)로 된 SLI code를 생성한 후 NEST simulation kernel을 제어한다.

NEural Simulation Tool (www.nest-initiative.org)은 대규모 이형 뉴런 네트워크를 시뮬레이션 하기 위해 설계된 GPL 라이선스 오픈 소스 소프트웨어이다. 시뮬레이터는 Python에 대한 interface를 제공한다. Figure 1은 사용자의 simulation script와 NEST Simulator 간의 상호작용을 묘사하고 있다. 높은 시뮬레이션 성능을 위해, 시뮬레이션 커널은 C++로 작성되었다.

파이썬에서 NEST API를 사용하고자 할 땐 import nest를 입력하면 된다. scikit-lean이나 scipy처럼 다른 package가 필요할 땐, 반드시 nest를 import하기 전에 import한다. dir(nest)를 입력하면 사용할 수 있는 함수(커맨드)들의 목록을 볼 수 있다. plot 기능을 사용하기 위해서는 Matplotlib를 import한다 (import matplotlib.pyplot as plt). 해당 라이브러리를 사용하면 결과를 display 또는 저장할 수 있다.


### 노드 만들기

- 모든 새 노드는 Create()함수로 만들 수 있다. 이 함수는 model(string), n(모델 개수. int, *optional*), params(dict or list, *optional*), positions(grid or free object, *optional*)를 인자로 받는다. <a href ="https://nest-simulator.readthedocs.io/en/stable/ref_material/pynest_apis.html#nest.lib.hl_api_nodes.Create">참조.</a> 함수의 반환값은 NodeCollection 오브젝트로, 정수값인 id로 대표된다. 대부분의 PyNEST 함수는 NodeCollection 오브젝트를 입력인자로 받거나 반환한다.

  - 사용할 수 있는 노드의 타입(즉, model 부분에 들어갈 string 타입의 이름)에는 다음과 같은 종류가 있다.
    - "iaf_psc_alpha": alpha-shaped postsynaptic current를 가진 integrate-and-fire 모델. [파라미터 참조](https://nest-simulator.readthedocs.io/en/v3.3/models/iaf_psc_alpha_ps.html)
    - "hh_psc_alpha": [파라미터 참조](https://nest-simulator.readthedocs.io/en/v3.5/models/hh_psc_alpha.html)
    - "ht_neuron": [파라미터 참조](https://nest-simulator.readthedocs.io/en/v3.5/models/ht_neuron.html)
    - 등등...
    - [더 많은 모델 종류는 이 링크 참조](https://nest-simulator.readthedocs.io/en/v3.5/models/)

  - 이를테면 neuron = nest.Create("iaf_pcs_alpha")는 새 IF모델 뉴런 하나를 만드는 코드이다. 이렇게 형성한 오브젝트는 get() 메서드를 사용해 각종 파라미터의 값을 확인할 수 있다. get()의 인자는 하나일 수도 있고 (string 타입. 이 경우 반환값은 floating point element이다.), 여러 개를 한꺼번에 참조할 수도 있다 (string list 타입. 이 경우 반환값은 입력 인자의 요소들에 각기 대응되는 dictionary이다.)

  - 반대로, set() 메서드를 사용하면 만들어진 오브젝터의 파라미터를 직접 수정할 수 있다. 예를 들면, neuron.set(I_e = 500.0) 또는 neuron.set({"I_e": 500.0})과 같은 형식으로 입력하면 된다. dictionary 타입을 이용하여 인자를 넣으면 여러 개의 파라미터를 한꺼번에 입력할 수 있다. 이 때 주의할 점은, **NEST는 type sensitive**하기 때문에 double type으로 정의된 값들은 반드시 타입에 맞춰서 넣어주어야 한다! (이를테면 500은 파이썬 인터프리터에서 정수로 인식되기 때문에, NEST 인터프리터에서 타입 오류를 유발한다.)

  - 


### 기본 연결로 노드 연결하기

### Device에서 데이터 추출하고 그래프 그리기

### 특수한 연결로 노드 연결하기

### 두 개의 연결된 뉴런

### 커맨드 정리