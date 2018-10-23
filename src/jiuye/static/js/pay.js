$("#mycom").click(function(){
	 var comtext = $("#comtext").val();
   	 $.post("../info/",{'comtext':comtext}, function(ret){ 
   		 	$("#containermain").html(ret);
       })

})

$("#mypay").click(function(){
	 var paytext = $("#paytext").val();
   	 $.post("../getpay/",{'paytext':paytext}, function(ret){ 
   		 	$("#containermain").html(ret); 	 		 	
       })
       	
})

$("#jiabtn").click(function(){
	 var text = $("#myinfo").text();
	 var intr = $("#myintr").text();
   	 $.post("../setjia/",{'text':text,'intr':intr}, function(ret){ 
   		 	$("#retsult").html(ret);
   		 	$("#jiabtn").attr("disabled", true);
   		 	$("#jianbtn").attr("disabled", true);
   		 	//$("#containermain").html(ret); 	 		 	
       })
       	
})
$("#jianbtn").click(function(){
	 var text = $("#myinfo").text();
	 var intr = $("#myintr").text();
   	 $.post("../setjian/",{'text':text,'intr':intr}, function(ret){ 
   		 	$("#retsult").html(ret);
   		 	$("#jiabtn").attr("disabled", true);
   		 	$("#jianbtn").attr("disabled", true);
   		 	//$("#containermain").html(ret); 	 		 	
       })
       	
})