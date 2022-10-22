<template>
  <div >
    <br>
    <el-row>
      <el-col v-for="App in AppList" span="1.5">
        <el-radio v-model="currentApp" :label="App" border>
          {{App}}
        </el-radio>
      </el-col>
      <el-col span="2">
      </el-col>
      <el-col span="1">
        <span class="text">请输入id：</span>
      </el-col>
      <el-col span="4">
        <el-input placeholder='请输入'></el-input>
      </el-col>
      <el-col span="4">
        <el-button type="primary" @click="searchInfo">查询</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col span="8">
        <div id="rate" :style="{width: '500px', height: '500px'}"></div>
      </el-col>
      <el-col span="16">
        <div id="bar" :style="{width: '1000px', height: '500px'}"></div>
      </el-col>
    </el-row>

    <img :src="wordcloudcode" >
    <div id="rel" :style="{width: '800px', height: '500px'}"></div>

  </div>
</template>

<script>

/* eslint-disable */
export default {
  data() {
    return {
      wordcloudcode:'',
      AppList:['全选','网易云','微博'],
      currentApp:'全选',
      rateChart:{
        tooltip: {
          formatter: '{a} <br/>{b} : {c}%'
        },
        series: [
          {
            name: 'Pressure',
            type: 'gauge',
            progress: {
              show: true
            },
            detail: {
              valueAnimation: true,
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
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [120, 200, 150, 80, 70, 110, 130,120, 200, 150, 80, 70, 110, 130],
            type: 'bar'
          }
        ]
      },
      categories:['1','2'],
      relChart:{
        // 图的标题
        title: {
          text: 'ECharts 关系图'
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
          symbolSize: 40, // 调整节点的大小
          roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [2, 10],
          force: {
            repulsion: 2500,
            edgeLength: [10, 50]
          },
          draggable: true,
          lineStyle: {
            normal: {
              width: 2,
              color: '#4b565b',
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
            name: 'node01',
            des: 'nodedes01',
            symbolSize: 70,
            category: 0,
          }, {
            name: 'node02',
            des: 'nodedes02',
            symbolSize: 50,
            category: 1,
          }, {
            name: 'node03',
            des: 'nodedes3',
            symbolSize: 50,
            category: 1,
          }, {
            name: 'node04',
            des: 'nodedes04',
            symbolSize: 50,
            category: 1,
          }, {
            name: 'node05',
            des: 'nodedes05',
            symbolSize: 50,
            category: 1,
          }],
          links: [{
            source: 'node01',
            target: 'node02',
            name: 'link01',
            des: 'link01des'
          }, {
            source: 'node01',
            target: 'node03',
            name: 'link02',
            des: 'link02des'
          }, {
            source: 'node01',
            target: 'node04',
            name: 'link03',
            des: 'link03des'
          }, {
            source: 'node01',
            target: 'node05',
            name: 'link04',
            des: 'link05des'
          }],
          categories: this.categories,
        }]
      }
    }
  },
  mounted() {
    this.draw();
    this.getWordCloud()
  },
  methods:{
    searchInfo(){
      this.getWordCloud()
    },
    draw(){
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
      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/wordCloud",
        data: '',
        responseType:'blob'
      }).then((response) => {
        this.wordcloudcode = window.URL.createObjectURL(response.data);
        console.log(this.cvcode)
      });
    },
  },
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
