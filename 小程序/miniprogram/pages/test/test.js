// pages/test/test.js

const app = getApp()
var that

Page({

  /**
   * 页面的初始数据
   */
  data: {
    num: 0,
    result: 1,
    imgData: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },
  bindInput: function (e) {
    this.setData({
      num: Number(e.detail.value)
    })
    console.log('input', this.data.num)
  },
  uploadPhoto() {
    var that = this;
    wx.chooseImage({
      count: 1, // 设置最多1张
      sizeType: ['compressed'], //所选的图片的尺寸
      sourceType: ['album', 'camera'], //选择图片的来源
      success(res) {
        wx.showToast({
          icon: "loading",
          title: "正在上传"
        })

        var tempFilePaths = res.tempFilePaths
        wx.uploadFile({
          url: 'http://101.226.18.132:8000/reg',
          // url: 'http://127.0.0.1:8080/reg',
          filePath: tempFilePaths[0],
          name: 'file',
          // formData: {
          //   'user': 'test'
          // },
          success: function (res) {
            var b64 = res.data
            // var array = wx.base64ToArrayBuffer(res.data);
            // var b64 = wx.arrayBufferToBase64(array);
            console.log(res)
            that.setData({
              imgData:'data:image/jpeg;base64,'+b64,

            })
          }
        })
      }
    })
  },

  sum: function () {
    that = this
    wx.request({
      url: 'http://101.226.18.132:8000/add',
      data: {
        num: that.data.num,
      },
      method: "post",
      success(res) {
        that.setData({
          result: res.data + 1,
        })
        // db.collection('test').add({
        //   data:{
        //     sum: res.data
        //   }

        // })
        // .then(res => {

        // })
        // .catch(console.error)

      }

    })

  },

})
