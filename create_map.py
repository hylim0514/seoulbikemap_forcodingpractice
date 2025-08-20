import os
import requests
import json
import pandas as pd
import folium

# GitHub Actions의 Secrets에 저장된 API 키를 환경 변수로 가져옵니다.
apikey = os.environ.get('SEOUL_OPENAPI_KEY')

# API 요청 URL 생성
startnum = 1
endnum = 1000
url = f'http://openapi.seoul.go.kr:8088/{apikey}/json/bikeList/{startnum}/{endnum}/'

try:
    json_data = requests.get(url).json()
    bike = pd.read_json(json.dumps(json_data['rentBikeStatus']['row']))
    
    # 지도 생성
    bike_map = folium.Map(location=[37.55, 126.98], zoom_start=12)

    # 마커 추가
    for name, lat, lng, cnt in zip(bike['stationName'], bike['stationLatitude'], bike['stationLongitude'], bike['parkingBikeTotCnt']):
        folium.Marker(
            location=[lat, lng],
            popup=folium.Popup(f"<div style='white-space: nowrap'>{name},{cnt}</div>", max_width=300),
            icon=folium.Icon(color='blue', icon='bike', prefix='fa')
        ).add_to(bike_map)

    # HTML 파일로 저장
    bike_map.save('bike_map.html')
    print("지도 파일이 성공적으로 생성되었습니다.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")
