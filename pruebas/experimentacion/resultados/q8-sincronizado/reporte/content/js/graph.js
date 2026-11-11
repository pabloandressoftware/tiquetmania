/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 71.0, "minX": 0.0, "maxY": 126273.0, "series": [{"data": [[0.0, 71.0], [0.1, 71.0], [0.2, 71.0], [0.3, 71.0], [0.4, 72.0], [0.5, 72.0], [0.6, 72.0], [0.7, 73.0], [0.8, 74.0], [0.9, 74.0], [1.0, 76.0], [1.1, 76.0], [1.2, 76.0], [1.3, 76.0], [1.4, 77.0], [1.5, 77.0], [1.6, 80.0], [1.7, 80.0], [1.8, 80.0], [1.9, 80.0], [2.0, 81.0], [2.1, 81.0], [2.2, 82.0], [2.3, 82.0], [2.4, 82.0], [2.5, 83.0], [2.6, 83.0], [2.7, 84.0], [2.8, 84.0], [2.9, 85.0], [3.0, 85.0], [3.1, 87.0], [3.2, 87.0], [3.3, 89.0], [3.4, 89.0], [3.5, 91.0], [3.6, 91.0], [3.7, 92.0], [3.8, 92.0], [3.9, 94.0], [4.0, 94.0], [4.1, 96.0], [4.2, 96.0], [4.3, 96.0], [4.4, 96.0], [4.5, 97.0], [4.6, 97.0], [4.7, 97.0], [4.8, 97.0], [4.9, 100.0], [5.0, 100.0], [5.1, 100.0], [5.2, 100.0], [5.3, 101.0], [5.4, 101.0], [5.5, 101.0], [5.6, 101.0], [5.7, 102.0], [5.8, 102.0], [5.9, 103.0], [6.0, 103.0], [6.1, 103.0], [6.2, 103.0], [6.3, 104.0], [6.4, 104.0], [6.5, 105.0], [6.6, 105.0], [6.7, 105.0], [6.8, 105.0], [6.9, 105.0], [7.0, 105.0], [7.1, 106.0], [7.2, 106.0], [7.3, 107.0], [7.4, 107.0], [7.5, 108.0], [7.6, 108.0], [7.7, 108.0], [7.8, 108.0], [7.9, 109.0], [8.0, 109.0], [8.1, 109.0], [8.2, 109.0], [8.3, 109.0], [8.4, 109.0], [8.5, 109.0], [8.6, 109.0], [8.7, 109.0], [8.8, 109.0], [8.9, 110.0], [9.0, 110.0], [9.1, 110.0], [9.2, 110.0], [9.3, 110.0], [9.4, 110.0], [9.5, 111.0], [9.6, 111.0], [9.7, 111.0], [9.8, 111.0], [9.9, 112.0], [10.0, 112.0], [10.1, 113.0], [10.2, 113.0], [10.3, 113.0], [10.4, 113.0], [10.5, 114.0], [10.6, 114.0], [10.7, 114.0], [10.8, 114.0], [10.9, 114.0], [11.0, 114.0], [11.1, 115.0], [11.2, 115.0], [11.3, 115.0], [11.4, 115.0], [11.5, 115.0], [11.6, 115.0], [11.7, 115.0], [11.8, 115.0], [11.9, 117.0], [12.0, 117.0], [12.1, 117.0], [12.2, 117.0], [12.3, 118.0], [12.4, 118.0], [12.5, 118.0], [12.6, 118.0], [12.7, 119.0], [12.8, 119.0], [12.9, 119.0], [13.0, 119.0], [13.1, 119.0], [13.2, 119.0], [13.3, 119.0], [13.4, 119.0], [13.5, 121.0], [13.6, 121.0], [13.7, 126.0], [13.8, 126.0], [13.9, 126.0], [14.0, 126.0], [14.1, 269.0], [14.2, 269.0], [14.3, 274.0], [14.4, 274.0], [14.5, 276.0], [14.6, 276.0], [14.7, 293.0], [14.8, 293.0], [14.9, 295.0], [15.0, 295.0], [15.1, 296.0], [15.2, 296.0], [15.3, 304.0], [15.4, 312.0], [15.5, 312.0], [15.6, 1055.0], [15.7, 1055.0], [15.8, 1055.0], [15.9, 1055.0], [16.0, 1056.0], [16.1, 1056.0], [16.2, 1058.0], [16.3, 1058.0], [16.4, 1058.0], [16.5, 1058.0], [16.6, 1058.0], [16.7, 1058.0], [16.8, 1059.0], [16.9, 1059.0], [17.0, 1059.0], [17.1, 1059.0], [17.2, 1063.0], [17.3, 1063.0], [17.4, 1064.0], [17.5, 1064.0], [17.6, 1065.0], [17.7, 1065.0], [17.8, 1108.0], [17.9, 1108.0], [18.0, 1110.0], [18.1, 1110.0], [18.2, 1111.0], [18.3, 1111.0], [18.4, 1130.0], [18.5, 1130.0], [18.6, 1132.0], [18.7, 1132.0], [18.8, 1133.0], [18.9, 1133.0], [19.0, 1134.0], [19.1, 1134.0], [19.2, 1134.0], [19.3, 1134.0], [19.4, 1138.0], [19.5, 1138.0], [19.6, 1139.0], [19.7, 1139.0], [19.8, 1140.0], [19.9, 1140.0], [20.0, 1257.0], [20.1, 1257.0], [20.2, 1261.0], [20.3, 1261.0], [20.4, 1263.0], [20.5, 1263.0], [20.6, 1264.0], [20.7, 1264.0], [20.8, 1264.0], [20.9, 1264.0], [21.0, 1266.0], [21.1, 1266.0], [21.2, 1268.0], [21.3, 1268.0], [21.4, 1269.0], [21.5, 1269.0], [21.6, 1269.0], [21.7, 1269.0], [21.8, 1269.0], [21.9, 1269.0], [22.0, 1270.0], [22.1, 1270.0], [22.2, 1273.0], [22.3, 1273.0], [22.4, 1274.0], [22.5, 1274.0], [22.6, 1279.0], [22.7, 1279.0], [22.8, 1321.0], [22.9, 1321.0], [23.0, 1330.0], [23.1, 1330.0], [23.2, 1331.0], [23.3, 1331.0], [23.4, 1334.0], [23.5, 1334.0], [23.6, 1335.0], [23.7, 1335.0], [23.8, 1336.0], [23.9, 1336.0], [24.0, 1337.0], [24.1, 1337.0], [24.2, 1337.0], [24.3, 1337.0], [24.4, 1338.0], [24.5, 1338.0], [24.6, 1338.0], [24.7, 1338.0], [24.8, 1341.0], [24.9, 1341.0], [25.0, 1341.0], [25.1, 1341.0], [25.2, 1341.0], [25.3, 1341.0], [25.4, 1342.0], [25.5, 1342.0], [25.6, 1345.0], [25.7, 1345.0], [25.8, 1554.0], [25.9, 1554.0], [26.0, 1560.0], [26.1, 1560.0], [26.2, 1562.0], [26.3, 1562.0], [26.4, 1563.0], [26.5, 1563.0], [26.6, 1565.0], [26.7, 1565.0], [26.8, 1573.0], [26.9, 1573.0], [27.0, 1575.0], [27.1, 1575.0], [27.2, 1580.0], [27.3, 1580.0], [27.4, 1581.0], [27.5, 1581.0], [27.6, 1581.0], [27.7, 1581.0], [27.8, 1583.0], [27.9, 1583.0], [28.0, 1584.0], [28.1, 1584.0], [28.2, 1584.0], [28.3, 1584.0], [28.4, 1587.0], [28.5, 1587.0], [28.6, 1587.0], [28.7, 1587.0], [28.8, 1645.0], [28.9, 1645.0], [29.0, 1647.0], [29.1, 1647.0], [29.2, 1648.0], [29.3, 1648.0], [29.4, 1649.0], [29.5, 1649.0], [29.6, 1650.0], [29.7, 1650.0], [29.8, 1701.0], [29.9, 1701.0], [30.0, 1731.0], [30.1, 1731.0], [30.2, 1732.0], [30.3, 1732.0], [30.4, 1736.0], [30.5, 1736.0], [30.6, 1737.0], [30.7, 1737.0], [30.8, 1737.0], [30.9, 1737.0], [31.0, 1738.0], [31.1, 1738.0], [31.2, 1738.0], [31.3, 1738.0], [31.4, 1743.0], [31.5, 1743.0], [31.6, 1744.0], [31.7, 1744.0], [31.8, 1745.0], [31.9, 1745.0], [32.0, 1746.0], [32.1, 1746.0], [32.2, 1746.0], [32.3, 1746.0], [32.4, 1748.0], [32.5, 1748.0], [32.6, 1749.0], [32.7, 1749.0], [32.8, 2048.0], [32.9, 2048.0], [33.0, 2050.0], [33.1, 2050.0], [33.2, 2051.0], [33.3, 2051.0], [33.4, 2054.0], [33.5, 2054.0], [33.6, 2054.0], [33.7, 2054.0], [33.8, 2057.0], [33.9, 2057.0], [34.0, 2058.0], [34.1, 2058.0], [34.2, 2059.0], [34.3, 2059.0], [34.4, 2061.0], [34.5, 2061.0], [34.6, 2062.0], [34.7, 2062.0], [34.8, 2063.0], [34.9, 2063.0], [35.0, 2066.0], [35.1, 2066.0], [35.2, 2066.0], [35.3, 2066.0], [35.4, 2067.0], [35.5, 2067.0], [35.6, 2069.0], [35.7, 2069.0], [35.8, 2148.0], [35.9, 2148.0], [36.0, 2148.0], [36.1, 2148.0], [36.2, 2149.0], [36.3, 2149.0], [36.4, 2151.0], [36.5, 2151.0], [36.6, 2151.0], [36.7, 2151.0], [36.8, 2153.0], [36.9, 2153.0], [37.0, 2157.0], [37.1, 2157.0], [37.2, 2159.0], [37.3, 2159.0], [37.4, 2349.0], [37.5, 2349.0], [37.6, 2353.0], [37.7, 2353.0], [37.8, 2353.0], [37.9, 2353.0], [38.0, 2353.0], [38.1, 2353.0], [38.2, 2360.0], [38.3, 2360.0], [38.4, 2360.0], [38.5, 2362.0], [38.6, 2362.0], [38.7, 2362.0], [38.8, 2362.0], [38.9, 2364.0], [39.0, 2364.0], [39.1, 2718.0], [39.2, 2718.0], [39.3, 2718.0], [39.4, 2718.0], [39.5, 2719.0], [39.6, 2719.0], [39.7, 2719.0], [39.8, 2719.0], [39.9, 2721.0], [40.0, 2721.0], [40.1, 2723.0], [40.2, 2723.0], [40.3, 2724.0], [40.4, 2724.0], [40.5, 3028.0], [40.6, 3028.0], [40.7, 3029.0], [40.8, 3029.0], [40.9, 3033.0], [41.0, 3033.0], [41.1, 3039.0], [41.2, 3039.0], [41.3, 3042.0], [41.4, 3042.0], [41.5, 3044.0], [41.6, 3044.0], [41.7, 3048.0], [41.8, 3048.0], [41.9, 3049.0], [42.0, 3049.0], [42.1, 3053.0], [42.2, 3053.0], [42.3, 3168.0], [42.4, 3168.0], [42.5, 3175.0], [42.6, 3175.0], [42.7, 3177.0], [42.8, 3177.0], [42.9, 3178.0], [43.0, 3178.0], [43.1, 3178.0], [43.2, 3178.0], [43.3, 3179.0], [43.4, 3179.0], [43.5, 3360.0], [43.6, 3360.0], [43.7, 3360.0], [43.8, 3360.0], [43.9, 3363.0], [44.0, 3363.0], [44.1, 3377.0], [44.2, 3377.0], [44.3, 3382.0], [44.4, 3382.0], [44.5, 3386.0], [44.6, 3386.0], [44.7, 3387.0], [44.8, 3387.0], [44.9, 4127.0], [45.0, 4127.0], [45.1, 4129.0], [45.2, 4129.0], [45.3, 4131.0], [45.4, 4131.0], [45.5, 4132.0], [45.6, 4132.0], [45.7, 4133.0], [45.8, 4133.0], [45.9, 4136.0], [46.0, 4136.0], [46.1, 4136.0], [46.2, 4136.0], [46.3, 4137.0], [46.4, 4137.0], [46.5, 4142.0], [46.6, 4142.0], [46.7, 4197.0], [46.8, 4197.0], [46.9, 4197.0], [47.0, 4197.0], [47.1, 4198.0], [47.2, 4198.0], [47.3, 4198.0], [47.4, 4198.0], [47.5, 4198.0], [47.6, 4198.0], [47.7, 4198.0], [47.8, 4198.0], [47.9, 4202.0], [48.0, 4202.0], [48.1, 4401.0], [48.2, 4401.0], [48.3, 4402.0], [48.4, 4402.0], [48.5, 4402.0], [48.6, 4402.0], [48.7, 4406.0], [48.8, 4406.0], [48.9, 4407.0], [49.0, 4407.0], [49.1, 4412.0], [49.2, 4412.0], [49.3, 4412.0], [49.4, 4412.0], [49.5, 4637.0], [49.6, 4637.0], [49.7, 4638.0], [49.8, 4638.0], [49.9, 4638.0], [50.0, 4638.0], [50.1, 4640.0], [50.2, 4640.0], [50.3, 4641.0], [50.4, 4641.0], [50.5, 4641.0], [50.6, 4641.0], [50.7, 4956.0], [50.8, 4956.0], [50.9, 4961.0], [51.0, 4961.0], [51.1, 4962.0], [51.2, 4962.0], [51.3, 4965.0], [51.4, 4965.0], [51.5, 4968.0], [51.6, 4968.0], [51.7, 4968.0], [51.8, 4968.0], [51.9, 4969.0], [52.0, 4969.0], [52.1, 4969.0], [52.2, 4969.0], [52.3, 4970.0], [52.4, 4970.0], [52.5, 4972.0], [52.6, 4972.0], [52.7, 4975.0], [52.8, 4975.0], [52.9, 5199.0], [53.0, 5199.0], [53.1, 5199.0], [53.2, 5199.0], [53.3, 5200.0], [53.4, 5200.0], [53.5, 5202.0], [53.6, 5202.0], [53.7, 5213.0], [53.8, 5213.0], [53.9, 5214.0], [54.0, 5214.0], [54.1, 5215.0], [54.2, 5215.0], [54.3, 5222.0], [54.4, 5222.0], [54.5, 5225.0], [54.6, 5225.0], [54.7, 5226.0], [54.8, 5226.0], [54.9, 5406.0], [55.0, 5406.0], [55.1, 5411.0], [55.2, 5411.0], [55.3, 5416.0], [55.4, 5416.0], [55.5, 5417.0], [55.6, 5417.0], [55.7, 5421.0], [55.8, 5421.0], [55.9, 5423.0], [56.0, 5423.0], [56.1, 5435.0], [56.2, 5435.0], [56.3, 5435.0], [56.4, 5435.0], [56.5, 6863.0], [56.6, 6863.0], [56.7, 6881.0], [56.8, 6881.0], [56.9, 6885.0], [57.0, 6885.0], [57.1, 6886.0], [57.2, 6886.0], [57.3, 6887.0], [57.4, 6887.0], [57.5, 6889.0], [57.6, 6889.0], [57.7, 6892.0], [57.8, 6892.0], [57.9, 7648.0], [58.0, 7648.0], [58.1, 7649.0], [58.2, 7649.0], [58.3, 7652.0], [58.4, 7652.0], [58.5, 7655.0], [58.6, 7655.0], [58.7, 7656.0], [58.8, 7656.0], [58.9, 7657.0], [59.0, 7657.0], [59.1, 7657.0], [59.2, 7657.0], [59.3, 7658.0], [59.4, 7658.0], [59.5, 8025.0], [59.6, 8025.0], [59.7, 8026.0], [59.8, 8026.0], [59.9, 8028.0], [60.0, 8028.0], [60.1, 8031.0], [60.2, 8031.0], [60.3, 8035.0], [60.4, 8035.0], [60.5, 8038.0], [60.6, 8038.0], [60.7, 8039.0], [60.8, 8039.0], [60.9, 8039.0], [61.0, 8039.0], [61.1, 8414.0], [61.2, 8414.0], [61.3, 8414.0], [61.4, 8414.0], [61.5, 8414.0], [61.6, 8414.0], [61.7, 8416.0], [61.8, 8416.0], [61.9, 8417.0], [62.0, 8417.0], [62.1, 8418.0], [62.2, 8418.0], [62.3, 8419.0], [62.4, 8419.0], [62.5, 8792.0], [62.6, 8792.0], [62.7, 8802.0], [62.8, 8802.0], [62.9, 8805.0], [63.0, 8805.0], [63.1, 8806.0], [63.2, 8806.0], [63.3, 8807.0], [63.4, 8807.0], [63.5, 8808.0], [63.6, 8808.0], [63.7, 8808.0], [63.8, 8808.0], [63.9, 8809.0], [64.0, 8809.0], [64.1, 12569.0], [64.2, 12569.0], [64.3, 12571.0], [64.4, 12571.0], [64.5, 12583.0], [64.6, 12583.0], [64.7, 12585.0], [64.8, 12585.0], [64.9, 12587.0], [65.0, 12587.0], [65.1, 12587.0], [65.2, 12587.0], [65.3, 15130.0], [65.4, 15130.0], [65.5, 15137.0], [65.6, 15137.0], [65.7, 15141.0], [65.8, 15141.0], [65.9, 15142.0], [66.0, 15142.0], [66.1, 15142.0], [66.2, 15142.0], [66.3, 15142.0], [66.4, 15142.0], [66.5, 15145.0], [66.6, 15145.0], [66.7, 15146.0], [66.8, 15146.0], [66.9, 15147.0], [67.0, 15147.0], [67.1, 15645.0], [67.2, 15645.0], [67.3, 15645.0], [67.4, 15645.0], [67.5, 15646.0], [67.6, 15646.0], [67.7, 15648.0], [67.8, 15648.0], [67.9, 15653.0], [68.0, 15653.0], [68.1, 15656.0], [68.2, 15656.0], [68.3, 15657.0], [68.4, 15657.0], [68.5, 16157.0], [68.6, 16157.0], [68.7, 16158.0], [68.8, 16158.0], [68.9, 16159.0], [69.0, 16159.0], [69.1, 16159.0], [69.2, 16159.0], [69.3, 16162.0], [69.4, 16162.0], [69.5, 16162.0], [69.6, 16162.0], [69.7, 16162.0], [69.8, 16162.0], [69.9, 16652.0], [70.0, 16652.0], [70.1, 16657.0], [70.2, 16657.0], [70.3, 16677.0], [70.4, 16677.0], [70.5, 16677.0], [70.6, 16677.0], [70.7, 16678.0], [70.8, 16678.0], [70.9, 16680.0], [71.0, 16680.0], [71.1, 16681.0], [71.2, 16681.0], [71.3, 16682.0], [71.4, 16682.0], [71.5, 16682.0], [71.6, 16682.0], [71.7, 26393.0], [71.8, 26393.0], [71.9, 26394.0], [72.0, 26394.0], [72.1, 26395.0], [72.2, 26395.0], [72.3, 26407.0], [72.4, 26407.0], [72.5, 26408.0], [72.6, 26408.0], [72.7, 26410.0], [72.8, 26410.0], [72.9, 29468.0], [73.0, 29468.0], [73.1, 29473.0], [73.2, 29473.0], [73.3, 29474.0], [73.4, 29474.0], [73.5, 29476.0], [73.6, 29476.0], [73.7, 29477.0], [73.8, 29477.0], [73.9, 29481.0], [74.0, 29481.0], [74.1, 29481.0], [74.2, 29481.0], [74.3, 29481.0], [74.4, 29481.0], [74.5, 29482.0], [74.6, 29482.0], [74.7, 29482.0], [74.8, 29482.0], [74.9, 30478.0], [75.0, 30478.0], [75.1, 30478.0], [75.2, 30478.0], [75.3, 30490.0], [75.4, 30490.0], [75.5, 30496.0], [75.6, 30496.0], [75.7, 30496.0], [75.8, 30496.0], [75.9, 30499.0], [76.0, 30499.0], [76.1, 30501.0], [76.2, 30501.0], [76.3, 30504.0], [76.4, 30504.0], [76.5, 30504.0], [76.6, 30504.0], [76.7, 30504.0], [76.8, 30504.0], [76.9, 31518.0], [77.0, 31518.0], [77.1, 31520.0], [77.2, 31520.0], [77.3, 31521.0], [77.4, 31521.0], [77.5, 31523.0], [77.6, 31523.0], [77.7, 32035.0], [77.8, 32035.0], [77.9, 32035.0], [78.0, 32035.0], [78.1, 32038.0], [78.2, 32038.0], [78.3, 32040.0], [78.4, 32040.0], [78.5, 32040.0], [78.6, 32040.0], [78.7, 32041.0], [78.8, 32041.0], [78.9, 32042.0], [79.0, 32042.0], [79.1, 32044.0], [79.2, 32044.0], [79.3, 57626.0], [79.4, 57626.0], [79.5, 57634.0], [79.6, 57634.0], [79.7, 57635.0], [79.8, 57635.0], [79.9, 57636.0], [80.0, 57636.0], [80.1, 57637.0], [80.2, 57637.0], [80.3, 57638.0], [80.4, 57638.0], [80.5, 57638.0], [80.6, 57638.0], [80.7, 59664.0], [80.8, 59664.0], [80.9, 59673.0], [81.0, 59673.0], [81.1, 59673.0], [81.2, 59673.0], [81.3, 59685.0], [81.4, 59685.0], [81.5, 59686.0], [81.6, 59686.0], [81.7, 59687.0], [81.8, 59687.0], [81.9, 59688.0], [82.0, 59688.0], [82.1, 62736.0], [82.2, 62736.0], [82.3, 62760.0], [82.4, 62760.0], [82.5, 62760.0], [82.6, 62760.0], [82.7, 62760.0], [82.8, 62760.0], [82.9, 62761.0], [83.0, 62761.0], [83.1, 62766.0], [83.2, 62766.0], [83.3, 62767.0], [83.4, 62767.0], [83.5, 113944.0], [83.6, 113944.0], [83.7, 113946.0], [83.8, 113946.0], [83.9, 113953.0], [84.0, 113953.0], [84.1, 113954.0], [84.2, 113954.0], [84.3, 113955.0], [84.4, 113955.0], [84.5, 113955.0], [84.6, 113955.0], [84.7, 113956.0], [84.8, 113956.0], [84.9, 113956.0], [85.0, 113956.0], [85.1, 118047.0], [85.2, 118047.0], [85.3, 126220.0], [85.4, 126220.0], [85.5, 126221.0], [85.6, 126221.0], [85.7, 126221.0], [85.8, 126221.0], [85.9, 126221.0], [86.0, 126221.0], [86.1, 126225.0], [86.2, 126225.0], [86.3, 126227.0], [86.4, 126227.0], [86.5, 126227.0], [86.6, 126227.0], [86.7, 126227.0], [86.8, 126227.0], [86.9, 126229.0], [87.0, 126229.0], [87.1, 126230.0], [87.2, 126230.0], [87.3, 126232.0], [87.4, 126232.0], [87.5, 126232.0], [87.6, 126232.0], [87.7, 126233.0], [87.8, 126233.0], [87.9, 126237.0], [88.0, 126237.0], [88.1, 126237.0], [88.2, 126237.0], [88.3, 126238.0], [88.4, 126238.0], [88.5, 126239.0], [88.6, 126239.0], [88.7, 126239.0], [88.8, 126239.0], [88.9, 126239.0], [89.0, 126239.0], [89.1, 126239.0], [89.2, 126239.0], [89.3, 126241.0], [89.4, 126241.0], [89.5, 126242.0], [89.6, 126242.0], [89.7, 126242.0], [89.8, 126242.0], [89.9, 126243.0], [90.0, 126243.0], [90.1, 126243.0], [90.2, 126243.0], [90.3, 126243.0], [90.4, 126243.0], [90.5, 126244.0], [90.6, 126244.0], [90.7, 126244.0], [90.8, 126244.0], [90.9, 126244.0], [91.0, 126244.0], [91.1, 126244.0], [91.2, 126244.0], [91.3, 126244.0], [91.4, 126244.0], [91.5, 126246.0], [91.6, 126246.0], [91.7, 126246.0], [91.8, 126246.0], [91.9, 126246.0], [92.0, 126246.0], [92.1, 126246.0], [92.2, 126246.0], [92.3, 126246.0], [92.4, 126246.0], [92.5, 126247.0], [92.6, 126247.0], [92.7, 126247.0], [92.8, 126247.0], [92.9, 126248.0], [93.0, 126248.0], [93.1, 126248.0], [93.2, 126248.0], [93.3, 126249.0], [93.4, 126249.0], [93.5, 126250.0], [93.6, 126250.0], [93.7, 126250.0], [93.8, 126250.0], [93.9, 126251.0], [94.0, 126251.0], [94.1, 126252.0], [94.2, 126252.0], [94.3, 126252.0], [94.4, 126252.0], [94.5, 126252.0], [94.6, 126252.0], [94.7, 126253.0], [94.8, 126253.0], [94.9, 126253.0], [95.0, 126253.0], [95.1, 126253.0], [95.2, 126253.0], [95.3, 126254.0], [95.4, 126254.0], [95.5, 126254.0], [95.6, 126254.0], [95.7, 126254.0], [95.8, 126254.0], [95.9, 126254.0], [96.0, 126254.0], [96.1, 126256.0], [96.2, 126256.0], [96.3, 126258.0], [96.4, 126258.0], [96.5, 126258.0], [96.6, 126258.0], [96.7, 126259.0], [96.8, 126259.0], [96.9, 126260.0], [97.0, 126260.0], [97.1, 126261.0], [97.2, 126261.0], [97.3, 126262.0], [97.4, 126262.0], [97.5, 126262.0], [97.6, 126262.0], [97.7, 126262.0], [97.8, 126262.0], [97.9, 126263.0], [98.0, 126263.0], [98.1, 126263.0], [98.2, 126263.0], [98.3, 126264.0], [98.4, 126264.0], [98.5, 126265.0], [98.6, 126265.0], [98.7, 126265.0], [98.8, 126265.0], [98.9, 126266.0], [99.0, 126266.0], [99.1, 126266.0], [99.2, 126266.0], [99.3, 126267.0], [99.4, 126267.0], [99.5, 126268.0], [99.6, 126268.0], [99.7, 126270.0], [99.8, 126270.0], [99.9, 126273.0], [100.0, 126273.0]], "isOverall": false, "label": "SeleccionTarifaYCantidad", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 0.0, "maxY": 74.0, "series": [{"data": [[0.0, 24.0], [1000.0, 11.0], [1100.0, 11.0], [1200.0, 14.0], [1300.0, 15.0], [1500.0, 15.0], [1600.0, 5.0], [1700.0, 15.0], [2000.0, 15.0], [2100.0, 8.0], [2300.0, 8.0], [2700.0, 7.0], [3000.0, 9.0], [3100.0, 6.0], [3300.0, 7.0], [4100.0, 15.0], [4200.0, 1.0], [4400.0, 7.0], [4600.0, 6.0], [4900.0, 11.0], [5100.0, 2.0], [5200.0, 8.0], [5400.0, 8.0], [6800.0, 7.0], [113900.0, 8.0], [7600.0, 8.0], [8000.0, 8.0], [8400.0, 7.0], [8700.0, 1.0], [8800.0, 7.0], [12500.0, 6.0], [15100.0, 9.0], [15600.0, 7.0], [16100.0, 7.0], [16600.0, 9.0], [100.0, 46.0], [26300.0, 3.0], [26400.0, 3.0], [29400.0, 10.0], [30400.0, 6.0], [30500.0, 4.0], [31500.0, 4.0], [32000.0, 8.0], [200.0, 6.0], [57600.0, 7.0], [59600.0, 7.0], [62700.0, 7.0], [300.0, 2.0], [118000.0, 1.0], [126200.0, 74.0]], "isOverall": false, "label": "SeleccionTarifaYCantidad", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 126200.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 51.0, "minX": 0.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 288.0, "series": [{"data": [[0.0, 78.0]], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [[1.0, 51.0]], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [[2.0, 288.0]], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [[3.0, 83.0]], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 3.0, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 69.60810810810811, "minX": 1.7944137E12, "maxY": 418.9487179487179, "series": [{"data": [[1.79441388E12, 69.60810810810811], [1.7944137E12, 418.9487179487179], [1.79441382E12, 84.5], [1.79441376E12, 199.06046511627895]], "isOverall": false, "label": "Usuarios (grupo principal)", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.79441388E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 118.50649350649351, "minX": 34.0, "maxY": 126273.0, "series": [{"data": [[34.0, 126273.0], [39.0, 126267.0], [53.0, 126269.0], [54.0, 126242.0], [56.0, 126266.0], [62.0, 126265.5], [63.0, 126265.0], [66.0, 126255.33333333333], [64.0, 126246.66666666667], [67.0, 126263.0], [69.0, 126252.78571428571], [75.0, 118047.0], [74.0, 126240.95238095238], [72.0, 126248.0], [83.0, 113952.14285714286], [80.0, 113954.0], [85.0, 62766.5], [90.0, 62760.333333333336], [88.0, 62748.0], [95.0, 59664.0], [94.0, 59686.5], [92.0, 59686.5], [97.0, 59673.0], [100.0, 57632.666666666664], [105.0, 32044.0], [104.0, 57636.5], [110.0, 32038.75], [114.0, 31522.0], [112.0, 32038.666666666668], [119.0, 30500.0], [118.0, 30496.0], [116.0, 31519.0], [121.0, 30499.0], [127.0, 29482.0], [126.0, 30487.5], [125.0, 30502.5], [135.0, 29468.0], [133.0, 29479.0], [132.0, 29481.0], [130.0, 29478.666666666668], [142.0, 26400.5], [141.0, 26394.0], [140.0, 26395.0], [139.0, 26408.5], [136.0, 29475.0], [151.0, 16669.0], [148.0, 16682.0], [147.0, 16672.666666666668], [144.0, 16679.5], [158.0, 16158.0], [157.0, 16158.5], [154.0, 16162.0], [167.0, 15144.5], [165.0, 15654.5], [164.0, 15645.0], [162.0, 15651.5], [161.0, 15645.0], [160.0, 15648.0], [174.0, 15135.5], [173.0, 15137.0], [172.0, 15142.0], [171.0, 15142.0], [170.0, 15145.0], [169.0, 15146.0], [182.0, 8809.0], [180.0, 12576.0], [178.0, 12581.0], [176.0, 12587.0], [188.0, 8797.0], [187.0, 8806.0], [186.0, 8805.0], [185.0, 8808.0], [184.0, 8807.0], [198.0, 8033.0], [195.0, 8414.0], [193.0, 8414.0], [192.0, 8417.5], [207.0, 7656.666666666667], [205.0, 7648.0], [203.0, 8030.0], [202.0, 8026.0], [201.0, 8039.0], [200.0, 8035.0], [213.0, 6889.0], [211.0, 7650.5], [210.0, 7656.0], [208.0, 7657.0], [223.0, 5435.0], [222.0, 5423.0], [221.0, 5435.0], [220.0, 5411.0], [218.0, 6883.0], [216.0, 6879.666666666667], [231.0, 5213.0], [229.0, 5214.5], [226.0, 5416.5], [225.0, 5406.0], [224.0, 5421.0], [239.0, 4968.0], [238.0, 4975.0], [236.0, 5205.0], [233.0, 5217.666666666667], [247.0, 4965.0], [245.0, 4970.5], [242.0, 4965.0], [240.0, 4961.0], [255.0, 4412.0], [253.0, 4637.666666666667], [251.0, 4640.0], [250.0, 4641.0], [270.0, 4136.0], [271.0, 4127.0], [269.0, 4142.0], [267.0, 4197.333333333333], [264.0, 4198.0], [263.0, 4198.0], [262.0, 4202.0], [260.0, 4406.0], [259.0, 4404.25], [256.0, 4407.0], [286.0, 3178.0], [287.0, 3168.0], [285.0, 3175.0], [283.0, 3379.5], [281.0, 3368.6666666666665], [279.0, 3363.0], [277.0, 3387.0], [276.0, 4132.5], [273.0, 4136.0], [272.0, 4132.0], [302.0, 2719.0], [301.0, 2721.0], [289.0, 3178.0], [299.0, 2723.0], [298.0, 3046.0], [297.0, 3033.0], [296.0, 3042.0], [295.0, 3049.0], [294.0, 3039.0], [293.0, 3053.0], [292.0, 3028.5], [317.0, 2157.0], [319.0, 2150.0], [316.0, 2156.0], [313.0, 2353.0], [310.0, 2355.5], [309.0, 2364.0], [308.0, 2361.0], [305.0, 2720.3333333333335], [304.0, 2718.0], [334.0, 2058.0], [335.0, 2057.0], [333.0, 2060.0], [330.0, 2057.6666666666665], [327.0, 2055.6666666666665], [325.0, 2066.0], [324.0, 2067.0], [323.0, 2069.0], [321.0, 2149.0], [339.0, 1746.0], [350.0, 1731.5], [351.0, 1701.0], [348.0, 1737.25], [346.0, 1737.0], [343.0, 1745.0], [341.0, 1745.0], [340.0, 1746.0], [338.0, 1749.0], [336.0, 2054.0], [365.0, 1582.0], [364.0, 1584.0], [363.0, 1584.0], [362.0, 1587.0], [360.0, 1573.3333333333333], [359.0, 1581.0], [356.0, 1645.0], [355.0, 1648.0], [353.0, 1650.0], [382.0, 1334.0], [383.0, 1338.0], [381.0, 1341.0], [379.0, 1336.3333333333333], [377.0, 1341.0], [376.0, 1326.0], [374.0, 1343.0], [371.0, 1566.6666666666667], [369.0, 1565.0], [368.0, 1567.0], [397.0, 1264.3333333333333], [394.0, 1268.6666666666667], [393.0, 1270.0], [391.0, 1274.0], [388.0, 1273.5], [386.0, 1335.0], [385.0, 1337.0], [414.0, 1063.5], [411.0, 1126.75], [407.0, 1118.3333333333333], [405.0, 1130.0], [403.0, 1139.0], [400.0, 1260.6666666666667], [422.0, 1055.5], [421.0, 1060.0], [418.0, 1058.0], [417.0, 1058.5], [416.0, 1059.0], [481.0, 312.0], [500.0, 118.50649350649351]], "isOverall": false, "label": "SeleccionTarifaYCantidad", "isController": false}, {"data": [[261.99200000000036, 28442.318000000017]], "isOverall": false, "label": "SeleccionTarifaYCantidad-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 500.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 0.0, "minX": 1.7944137E12, "maxY": 3207.9, "series": [{"data": [[1.79441388E12, 3207.9], [1.7944137E12, 893.65], [1.79441382E12, 422.06666666666666], [1.79441376E12, 985.9666666666667]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.79441388E12, 0.0], [1.7944137E12, 789.4833333333333], [1.79441382E12, 28.25], [1.79441376E12, 871.55]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.79441388E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 1006.0256410256412, "minX": 1.7944137E12, "maxY": 126247.37837837839, "series": [{"data": [[1.79441388E12, 126247.37837837839], [1.7944137E12, 1006.0256410256412], [1.79441382E12, 91811.0], [1.79441376E12, 14947.451162790698]], "isOverall": false, "label": "SeleccionTarifaYCantidad", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.79441388E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 0.0, "minX": 1.7944137E12, "maxY": 27456.75, "series": [{"data": [[1.79441388E12, 0.0], [1.7944137E12, 1005.8512820512817], [1.79441382E12, 27456.75], [1.79441376E12, 14947.311627906976]], "isOverall": false, "label": "SeleccionTarifaYCantidad", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.79441388E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 773.4666666666668, "minX": 1.7944137E12, "maxY": 2735.3720930232557, "series": [{"data": [[1.79441388E12, 1123.8513513513517], [1.7944137E12, 773.4666666666668], [1.79441382E12, 1827.1250000000002], [1.79441376E12, 2735.3720930232557]], "isOverall": false, "label": "SeleccionTarifaYCantidad", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.79441388E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 71.0, "minX": 1.7944137E12, "maxY": 62767.0, "series": [{"data": [[1.7944137E12, 2364.0], [1.79441382E12, 62767.0], [1.79441376E12, 59688.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.7944137E12, 71.0], [1.79441382E12, 62736.0], [1.79441376E12, 2718.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.7944137E12, 2066.0], [1.79441382E12, 62767.0], [1.79441376E12, 32035.0]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.7944137E12, 2362.08], [1.79441382E12, 62767.0], [1.79441376E12, 59686.84]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.7944137E12, 1138.0], [1.79441382E12, 62760.0], [1.79441376E12, 8038.0]], "isOverall": false, "label": "Median", "isController": false}, {"data": [[1.7944137E12, 2157.4], [1.79441382E12, 62767.0], [1.79441376E12, 57636.2]], "isOverall": false, "label": "95th percentile", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.79441382E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 108.5, "minX": 1.0, "maxY": 126247.0, "series": [{"data": [[8.0, 8806.5], [35.0, 5199.0], [9.0, 15899.5], [10.0, 29980.0], [12.0, 32036.5], [51.0, 1264.0], [14.0, 15907.0], [66.0, 1747.0], [78.0, 108.5], [23.0, 6030.0], [6.0, 19490.0], [7.0, 58651.0], [29.0, 3049.0]], "isOverall": false, "label": "Successes", "isController": false}, {"data": [[8.0, 113954.5], [1.0, 118047.0], [74.0, 126247.0]], "isOverall": false, "label": "Failures", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 78.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 0.0, "minX": 1.0, "maxY": 58651.0, "series": [{"data": [[8.0, 8806.5], [35.0, 5199.0], [9.0, 15899.5], [10.0, 29980.0], [12.0, 32036.5], [51.0, 1264.0], [14.0, 15906.5], [66.0, 1746.5], [78.0, 108.0], [23.0, 6029.5], [6.0, 19490.0], [7.0, 58651.0], [29.0, 3049.0]], "isOverall": false, "label": "Successes", "isController": false}, {"data": [[8.0, 0.0], [1.0, 0.0], [74.0, 0.0]], "isOverall": false, "label": "Failures", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 78.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 8.333333333333334, "minX": 1.7944137E12, "maxY": 8.333333333333334, "series": [{"data": [[1.7944137E12, 8.333333333333334]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7944137E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 0.11666666666666667, "minX": 1.7944137E12, "maxY": 3.5833333333333335, "series": [{"data": [[1.7944137E12, 3.25], [1.79441382E12, 0.11666666666666667], [1.79441376E12, 3.5833333333333335]], "isOverall": false, "label": "201", "isController": false}, {"data": [[1.79441388E12, 1.2333333333333334], [1.79441382E12, 0.15]], "isOverall": false, "label": "Non HTTP response code: java.net.SocketException", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.79441388E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 0.11666666666666667, "minX": 1.7944137E12, "maxY": 3.5833333333333335, "series": [{"data": [[1.79441388E12, 1.2333333333333334], [1.79441382E12, 0.15]], "isOverall": false, "label": "SeleccionTarifaYCantidad-failure", "isController": false}, {"data": [[1.7944137E12, 3.25], [1.79441382E12, 0.11666666666666667], [1.79441376E12, 3.5833333333333335]], "isOverall": false, "label": "SeleccionTarifaYCantidad-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.79441388E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 0.11666666666666667, "minX": 1.7944137E12, "maxY": 3.5833333333333335, "series": [{"data": [[1.7944137E12, 3.25], [1.79441382E12, 0.11666666666666667], [1.79441376E12, 3.5833333333333335]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [[1.79441388E12, 1.2333333333333334], [1.79441382E12, 0.15]], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.79441388E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, -18000000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

