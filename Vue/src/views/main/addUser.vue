<template>
    <div style="margin-top: 30px;margin-left: 50px">

      <el-input
        v-model="fetchIdStr"
        clearable
        remote
        placeholder="请输入用户id"
        style="width: 200px"
      >
      </el-input>
      <el-button type="primary" @click="catchById">
        爬取
      </el-button>
      <el-table
        :data="progressList"
        border
        fit
        highlight-current-row
        style="width: 304px"
      >
        <el-table-column
          label="id"
          prop="id"
          align="center"
          width="200"
        >
          <template slot-scope="{ row }">
            <span>{{ row[0] }}</span>
          </template>
        </el-table-column>

        <el-table-column
          label="爬取进度"
          prop="progress"
          align="center"
          width="100"
        >
          <template slot-scope="{ row }">
            <el-tag :type="row.progress ">
              {{ row[1] }}%
            </el-tag>
          </template>
        </el-table-column>

      </el-table>
    </div>
</template>
<script>

export default {
  data() {
    return {
      fetchIdStr:'',
      progressList:[],
    }
  },
  mounted() {
    this.fetchTable()
  },
  methods: {
    catchById() {
      let query=this.fetchIdStr
      if (query !== '') {
        this.axios.get('http://127.0.0.1:5000/catchById', {
          params: {
            strId: query
          }
        })
      }
    },
    fetchTable(){
      this.axios({
        method: "GET",
        url: "http://127.0.0.1:5000/get_1s",
      }).then((response) => {
        this.progressList = response.data;
      });
    }
  }
};
</script>

