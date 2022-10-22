<template>
  <div >
    <br>
    <el-row>
      <el-col v-for="App in AppList" :span=1.5>
        <el-radio v-model="currentApp" :label="App" border>
          {{App}}
        </el-radio>
      </el-col>
      <el-col :span=2>
      </el-col>
      <el-col :span=1>
        <span class="text">请输入id：</span>
      </el-col>
      <el-col :span=2>
        <el-select
          v-model="idStr"
          filterable
          clearable
          remote
          placeholder="请输入用户id"
          :remote-method="searchById"
          :idLoading="idLoading"
        >
          <el-option
            v-for="item in idList"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-col>
      <el-col :span=1>
        <el-button type="primary" @click="searchInfo">查询</el-button>
      </el-col>
      <el-col :span=1>
        <el-button type="primary" @click="dialogVisible=true">爬取新数据</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span=8>
        <div id="rate" :style="{width: '500px', height: '500px'}"></div>
      </el-col>
      <el-col :span=16>
        <div id="rel" :style="{width: '1000px', height: '500px'}"></div>
      </el-col>
    </el-row>
    <div>
      <el-row>
        <el-col :span=8>
          <img :src="wordCloudCode" style="margin-left: 60px">
        </el-col>
        <el-col :span=16 style="margin-top: -40px">
          <div id="bar" :style="{width: '1000px', height: '500px'}"></div>
        </el-col>
      </el-row>
      <el-dialog :visible.sync="dialogVisible" title="新增爬取">
        <fetch-data></fetch-data>
      </el-dialog>
    </div>



  </div>
</template>

<script>
import fetchData from './addUser'

/* eslint-disable 对外输出本模块*/
export default {
  components:{fetchData},
  data() {
    return {
      dialogVisible:false,
      idList: [],
      idStr:'',
      idLoading:false,
      wordCloudCode:'',
      AppList:['微博','网易云'],
      currentApp:'网易云',
      rateChart:{
        series: [
          {
            type: 'gauge',
            detail: {
              formatter: '{value}'+'分'
            },
            data: [
              {
                value: 75,
                name: '信用'
              }
            ]
          }
        ]
      },
      barChart:{
        xAxis: {
          type: 'category',
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ]
      },
      categories:[0,1],
      relChart:{
        // 图的标题
        title: {
          text: ''
        },
        // 提示框的配置
        tooltip: {
          formatter: function (x) {
            return x.data.des;
          }
        },
        // 工具箱
        toolbox: {
          // 显示工具箱
          show: true,
          feature: {
            mark: {
              show: true
            },
            // 还原
            restore: {
              show: true
            },
            // 保存为图片
            saveAsImage: {
              show: true
            }
          }
        },
        series: [{
          type: 'graph', // 类型:关系图
          layout: 'force', //图的布局，类型为力导图
          symbolSize: 50, // 调整节点的大小
          roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [2, 10],
          force: {
            repulsion: 250,
            edgeLength: [30,270],
          },
          draggable: true,
          itemStyle: {
            normal: {
              color: function (params) {
                let colorList = ['#FF69B4','#87CEEB'];
                return colorList[params.dataIndex]
              },
            }
          },
          lineStyle: {
            normal: {
              width: 4,
              color: 'source',
            }
          },
          edgeLabel: {
            normal: {
              show: true,
              formatter: function (x) {
                return x.data.name;
              }
            }
          },
          label: {
            normal: {
              show: true,
              textStyle: {}
            }
          },

          // 数据
          data: [{
            name: '木子魚_',
            symbolSize: 100,
            category: 0,
          }, {
            name: '云雀叫了w',
            category: 1,
          }, {
            name: '-_小金鱼睡不醒',
            category: 1,
          }, {
            name: '男孩陈天',
            category: 1,
          }, {
            name: '最爱霉霉',
            category: 1,
          }],
          links: [{
            source: '木子魚_',
            target: '云雀叫了w',
            name: '',
          },{
            source: '云雀叫了w',
            target: '木子魚_',
            name: '',
          }, {
            source: '木子魚_',
            target: '-_小金鱼睡不醒',
            name: '',
          }, {
            source: '-_小金鱼睡不醒',
            target: '男孩陈天',
            name: '',
          },{
            source: '木子魚_',
            target: '男孩陈天',
            name: '',
          }, {
            source: '木子魚_',
            target: '最爱霉霉',
            name: '',
          }],
          categories: this.categories,
        }]
      }
    }
  },
  created() {
  },
  mounted() {
    this.searchInfo()
    this.draw()
  },
  methods:{
    searchById(query) {
      // 根据输入的名称模糊匹配查询媒体名称
      if (query !== '') {
        this.idLoading = true;
        this.axios.get('http://127.0.0.1:5000/searchId', {
          params: {
            currentApp:this.currentApp,
            strId: query
          }
        }).then(res => {
          this.idList = res.data;
          this.idLoading = false;
        }).catch(
          error => {
            this.idList = [];
            this.idLoading = false;
            console.log(error);
          }
        );
      }
      else {
        this.idList = [];
      }
    },
    searchInfo(){
      this.getWordCloud()
      this.getBarChart()
      this.getRateChart()
      this.getRelChart()
      this.draw()
    },
    draw(){
      console.log(this.barChart)
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(document.getElementById('rate'))
      // 绘制图表
      myChart.setOption(this.rateChart);

      myChart = this.$echarts.init(document.getElementById('bar'))
      // 绘制图表
      myChart.setOption(this.barChart);
      myChart = this.$echarts.init(document.getElementById('rel'))
      // 绘制图表
      myChart.setOption(this.relChart);
    },
    getWordCloud(){
      this.axios.get("http://127.0.0.1:5000/wordCloud",{
        params: {
          currentApp:this.currentApp,
          strId: this.idStr
        },
        responseType:'blob'
      }).then((response) => {
        this.wordCloudCode = window.URL.createObjectURL(response.data);
      });
    },
    getBarChart(){
        this.axios.get('http://127.0.0.1:5000/getBarChart', {
          params: {
            currentApp:this.currentApp,
            strId: this.idStr
          }
        }).then(res => {
          this.barChart.xAxis.data = res.data[0];
          this.barChart.series[0].data=res.data[1]
          let myChart = this.$echarts.init(document.getElementById('bar'))
          // 绘制图表
          myChart.setOption(this.barChart);
        })
      },
    getRateChart(){
      this.axios.get('http://127.0.0.1:5000/getRateChart', {
        params: {
          currentApp:this.currentApp,
          strId: this.idStr
        }
      }).then(res => {
        this.rateChart.series[0].data[0].value=res.data
        let myChart = this.$echarts.init(document.getElementById('rate'))
        // 绘制图表
        myChart.setOption(this.rateChart);
      })
    },
    getRelChart(){
      this.axios.get('http://127.0.0.1:5000/getRelChart', {
        params: {
          currentApp:this.currentApp,
          strId: this.idStr
        }
      }).then(res => {
        this.relChart.series[0].data = res.data[0];
        this.relChart.series[0].links=res.data[1];
        let myChart = this.$echarts.init(document.getElementById('rel'))
        // 绘制图表
        myChart.setOption(this.relChart);
      })
    },
    }

}
</script>
<style type="text/css">
.el-col{
  min-height: 1px;
}
.text {
  font-size: 14px;
  color: #606266;
  line-height: 40px;
}
</style>
