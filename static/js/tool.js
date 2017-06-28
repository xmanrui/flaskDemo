/**
 * Created by pc on 2017/3/9.
 */

jQuery.extend({
    IsInArr: function (arr, value) {
         for(var i in arr)
        {
            if(arr[i] == value)
            {
                return true;
            }
        }

        return false;
    },
    GetOptionTextArr: function (option_in_select) {
        var optObj = $(option_in_select); // 如option_in_select = ".src-video option"
        var origin_opt = new Array();
        optObj.each(function (i, field){
                origin_opt[i] = $(this).text();
                });

        return origin_opt;
    }
});