// pages/travel/travel.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //定义查询一分一段表还是录取成绩，默认值false为查询录取成绩
    rankOrAdmission:false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },

  clickButton: function (e) {
    var res = wx.getStorageSync('res');
    this.setData({ res: res },);
  },

  changeRankOrAdmission:function(e){
    if (e.detail.value == "rank"){
      this.setData({
        rankOrAdmission: true,
      })
    }else{
      this.setData({
        rankOrAdmission: false,
      })
    }
    this.setData({
      res:[]
    })

    console.log(this.data.rankOrAdmission);
  },

  formSubmit: function(event) {
    console.log("提交表单");
    console.log(event.detail.value);
    this.setData({ res: [], });
    var that=this;
    var url = 'http://localhost:5000/' + event.detail.value.scienceorliberalarts;
    console.log(event.detail.value.rankoradmission);
    (event.detail.value.rankoradmission == "rank")?
      url = url+"rank":
      url= url;
    console.log(url);
    wx.request({
      url: url,
      data: {
        schoolname: event.detail.value.schoolname,
        maxscore: event.detail.value.maxscore,
        minscore: event.detail.value.minscore,
        year: event.detail.value.year,
      },
      method: 'POST',
      header: { 'content-type': 'application/x-www-form-urlencoded' },
      success: function (res) {
        wx.hideLoading();
        console.log(res.data, 'category data acquisition success');
        that.setData({ res: res.data, });
      },
      fail: function (res) {
        console.log('submit fail');
      },
      complete: function (res) {
        console.log('submit complete');
      }
    });
    wx.redirectTo({
      url: 'pages/databind/databind'
    });
  },

  formReset: function() {
    console.log("Form reset");
  }
})