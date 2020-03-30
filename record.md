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
