# Development Record Notes

## ◉ 3/27 1st Day

- 기본적인 Hyper Parameter 구현

  - planet_radius, planet_theta, angular_velocity
  - time, n
  - deceleration, fuel_to_acceleration

- function about plotting

  - draw_orbit : 행성 궤도 그리기
  - draw_planet : 행성 그리기
  - animate : 영상 구현

- func. move_planet()  
  시간이 지남에 따라 행성이 원운동하는 모습 구현

- func. calc_gravity()  
  중력을 구현하고 속도, 위치를 업데이트

- func. calc_value()  
  목적 행성과의 거리와 남은 연료량을 바탕으로 가치함수 계산

- func. first_make()  
  맨 처음 ship 제작

- func. make_children()  
  weight를 매개변수로 받고 ship 생성

- weight 자료구조 수정  
  (2, n) shape 으로 fuel_for_accel, fuel_for_rotate로 처음에 구성
  나중에는 시간에 따른 분석을 위해 (n, 2) shape으로 바꾸고 fuel_for_accel_x, fuel_for_accel_y 로 수정

- set the information of ship
  - x, y : x, y좌표
  - fuel : 연료량
  - v_x, v_y : x, y 방향 속도
  - weights : x, y 방향 가속에 쓸 연료(n, 2)
  - value : 가치함수
  - calc : 연산 여부

## ◉ 3/28 2nd Day

- func. move_ship()

  - 종료조건 설정

    - (0, 0)으로부터 21 이상 벗어났을 때
    - 연료가 0 이하일 때
    - 어느 행성에 충돌했을 때
    - 목적행성에 도달했을 때(isgood=True)

  - moment에 따른 weight concate  
    weight.shape[0]보다 moment가 같거나 크면 임의로 단위 weight를 생성하고 concate

  - ɛ-greedy 알고리즘 구현  
    ɛ값에 따라 정해진 weight 말고 다른 값을 따름

- planet_theta_init  
  planet_theta를 초기화할 때 다순히 등호로 할당할 경우 메로리를 공유하는 것으로 판단됨. planet_theta_init.copy()이용할 것

- func. test_ship()  
  가장 좋은 배의 정보를 바탕으로 영상 구현

- 초기값 설정  
  시작행성의 연직 방향으로 1만큼 떨어진 곳에서 연직 방향으로 0.8의 속도를 가짐((0, 0)으로부터 반대방향).

- Repeating Failiure  
  지속적으로 실패함. 주로 출발행성에 도로 충돌하는 양상을 보임.
  step마다 자식들을 만들어서 weight를 업데이트할 계획

## ◉ 3/29 3rd Day

- First Success!  
  처음으로 목적행성에 도달한 영상을 뽑아냄! ㅊㅋㅊㅋ😆  
  그러나 ship['isgood'] = True 인데도 목적행성에 도달하지 않는 현상이 지속적으로 발생

- Scale control  
  기존의 plotting area의 배율 scale을 정의하고 1 부터 2 사이의 값으로 조절해가며 구동.  
  1에 가까울 때만 ship['isgood'] = True 가 관찰됨.

- Duration of time  
  학습 방식을 바꿈. 만약 time = 151 이면 10step, 20step, 30step,⋯ 으로 10개씩 나눠서 학습  
  duration 마다 isgood 여부를 검사하고 isgood이 있다면 그중에서 가장 value가 높은 배를, 없다면 전체 중 value가 가장 높은 배를 부모로 하여 자식을 생산한다.  
  처음 step은 계속 update하면서 더 견고해지고 이전의 좋은 배를 부모로 계속 자식을 생산하기 때문에 더 좋을 것이라 예상함.

- total_best_ship, best_ship

  - total_best_ship  
    모든 epoch를 통틀어서 가장 좋은 배  
    isgood = True인 배중 가장 value가 높음  
    (weight, value) tuple

  - best_ship  
    한 epoch에서 가장 좋은 배  
    duration 마다 자식생산할 때 부모가 됨  
    (weight, value) tuple

- ship_exist  
  total_best_ship, best_ship의 여부를 저장하는 boolean  
  처음 (0, -1)로 저장하므로 best_ship[0]으로 업데이트 여부 판단하려 했으나 ValueError 발생

- how_far, how_fast  
  how_far: 맨 처음 start_planet에서 얼마나 멀리 떨어져 시작할지  
  how_fast: 맨 처음 속력, weight 생성 시 random 범위

- epsilon = 0  
  ɛ이 정확한 궤도운동에 방해된다고 판단하여 일단 0으로 수정

## ◉ 3/30 4th Day

- func. value  
  기존에 fuel / distance**4 에서 fuel을 빼고 start_planet을 넣음  
  distance(start_planet) / distance(target_planet)**3

  이것만 바꿨는데 바로 뽑은 영상 둘 다 성공함!!!

- fibonacci duration
  이전 duration 은 range(10, time, 10)이었는데 이를 time 보다 작은 피보나치 수로 바꿈

  획기적인 개선이 일어났다😍  
  middle_planet의 swingby, 정확한 궤도 추적까지!!!

- progression with duration  
  duration을 피보나치 수열, 계차수열, 등차수열 등으로 바꿔가며 구동

  결과적으로 어떤 수열을 사용하느냐보다 초기값이 1인 게 중요👌  
  또한 그 간격이 작은 게 중요👌  
  그래야 지구 중력을 이용하지 않고 운동함

- func. fibo, func. diff_of_progression  
  fibo: 주어진 수보다 작은 피보나치 수들로 이루어진 수열을 리턴  
  diff_of_progression: 한계치와 계차수열의 공차를 입력받고 주어진 수보다 작으면서 계차수열을 이루는 수열을 리턴
