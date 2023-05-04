/**
 * Vvveb
 *
 * Copyright (C) 2021  Ziadin Givan
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 */
 
if (VvvebTheme === undefined) var VvvebTheme = {};

VvvebTheme.Ajax = {
	call: function(parameters, element, callback) {

		$.ajax({
			url: '/index.php?module=' +  parameters["module"] + '&_component_ajax=' + parameters["component"] + '&_component_id=0&action=' + parameters["action"],
			type: 'post',
			data: parameters,
			//dataType: 'json',
			beforeSend: function() {
				$('.loading', element).removeClass('d-none');
				$('.button-text', element).addClass('d-none');
				if ($(element).is('button'))  {
					$(element).attr("disabled", "true");
				}
			},
			complete: function() {
				$('.loading', element).addClass('d-none');
				$('.button-text', element).removeClass('d-none');
				if ($(element).is('button')) {
					$(element).removeAttr("disabled");
				}
				//$('#cart > button').button('reset');
			},
			success: function(data) {
				//$("header [data-v-component-cart]")[0].outerHTML = data;
				if (callback) callback(data);
			},
			error: function(xhr, ajaxOptions, thrownError) {
				alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);
			}
		});		
		
	}
}

VvvebTheme.Cart = {
	
	module: 'cart/cart',
	component: 'cart',
	component_id: '0',
	
	ajax: function(action, parameters, element, callback) {
		parameters['module'] = this.module;
		parameters['action'] = action;
		parameters['component'] = this.component;
		VvvebTheme.Ajax.call(parameters, element, callback);
	},
	
	add: function(productId, quantity, element, callback) {
		return this.ajax('add',{'product_id':productId, 'quantity':quantity}, element, function (data) {
			let miniCart = $("header [data-v-component-cart]");
			if (miniCart.lenght) {
				miniCart[0].outerHTML = data;
			}
			if (callback) {
				callback();
			}
		});
	},
	
	update: function(productId, quantity) {
		return this.ajax('update',{'product_id':productId, 'quantity':quantity});
	},
	
	remove: function(productId, element, callback) {
		return this.ajax('remove', {'product_id':productId}, callback);
	}
}
VvvebTheme.Comments = {
	
	module: 'content/post',
	
	ajax: function(action, parameters, element, callback) {
		parameters['module'] = this.module;
		parameters['action'] = action;
		VvvebTheme.Ajax.call(parameters, element, callback);
	},
	
	add: function(parameters, element, callback) {
		return this.ajax('addComment',parameters, element, callback);
	},
	
	update: function(productId, quantity) {
		return this.ajax('update',{'product_id':productId, 'quantity':quantity});
	},
	
	remove: function(productId) {
		return this.ajax('remove', {'product_id':productId});
	}
}

VvvebTheme.User = {
	
	module: 'user/login',
	component: 'user',
	component_id: '0',
	
	ajax: function(action, parameters, element, callback) {
		parameters['module'] = this.module;
		parameters['action'] = action;
		parameters['component'] = this.component;
		VvvebTheme.Ajax.call(parameters, element, callback);
	},
	
	login: function(parameters, element, callback) {
		return this.ajax('index' ,parameters, element, callback);
	},
}

VvvebTheme.Search = {
	
	module: 'search',
	component: 'search',
	component_id: '0',
	
	ajax: function(action, parameters, element, callback) {
		parameters['module'] = this.module;
		parameters['action'] = action;
		parameters['component'] = this.component;
		VvvebTheme.Ajax.call(parameters, element, callback);
	},
	
	query: function(parameters, element, callback) {
		return this.ajax('index' ,parameters, element, callback);
	},
}

VvvebTheme.Alert  = {
	
	show: function(message) {
		$('.alert-top .message').html(message);
		$('.alert-top').addClass("show").css('display', 'block');
		
		setTimeout(function () {
			$('.alert-top').fadeOut();
		}, 4000);
	}
}

$('.alert-top').on('close.bs.alert', function (e) {
    e.preventDefault();
    $(this).removeClass('show').css('display', 'none');
});

VvvebTheme.Gui = {
	
	init: function() {
		var events = [];
		
		$("[data-v-vvveb-action]").each(function () {

			var on = "click";
			if (this.dataset.vVvvebOn) on = this.dataset.vVvvebOn;
			var event = '[data-v-vvveb-action="' + this.dataset.vVvvebAction + '"]';

			if (events.indexOf(event) > -1) return;
			events.push(event);

			$(document).on(on, event, VvvebTheme.Gui[this.dataset.vVvvebAction]);
		});
		/*
		for (actionName in VvvebTheme.Gui)
		{
			if (actionName == "init") continue;
			//console.log(actionName);
			$(document).on("click", '[data-v-vvveb-action="' + actionName + '"]', VvvebTheme.Gui[actionName]);
		}*/
	},
	
	addToCart : function (e) {
		var product = $(this).parents("[data-v-product],[data-v-component-product]");
		var img = $("img[data-v-product-image], img[data-v-product-image-src], img[data-v-product-image]", product);
		var name = $("[data-v-product-name]", product).text();
		var id = this.dataset.product_id;

		if (!id) {
			id = product[0].dataset.product_id;
			if (!id) {
				id = $('input[name="product_id"]', product).val();
			}
		}
		
		let cart_add_text = 'was added to cart';

		VvvebTheme.Cart.add(id, 1, this, function() {
			let src = img.attr("src");
			VvvebTheme.Alert.show(`
			<div class="clearfix">
				<img  class="float-start me-2" height="80" src="${src}"> &ensp; 
				<div class="float-start"><a href="#">${name}<a><br> <span class="text-muted">${cart_add_text}<span></span></div>
			</div>
			<div class="row mt-2 g-2 " data-v-if="cart.total_items">
				  <div class="col-6">
					<a href="/cart" class="btn btn-light btn-sm border w-100" data-v-url="cart/cart/index">
					  <i class="la la-shopping-cart la-lg"></i>
					  <span>View cart</span>
					</a>
				  </div>
				  <div class="col-6">
					<a href="/checkout" class="btn btn-primary btn-sm w-100" data-v-url="checkout/checkout/index">
					  <span>Checkout</span>
					  <i class="la la-arrow-right la-lg"></i>
					</a>
				  </div>
			</div>`);
		});
		
		return false;
	},	
	
	removeFromCart : function (e) {
		
		var product = $(this).parents("[data-v-product],[data-v-component-product], [data-v-cart-product]");
		var img = $("[data-v-product-image],[data-v-product-image], [data-v-cart-product-img]", product).attr("src");
		var name = $("[data-v-product-name]", product).text();
		var id = this.dataset.product_id;

		if (!id) {
			id = product[0].dataset.product_id;
			if (!id) {
				id = $('input[name="product_id"]', product).val();
			}
		}
		VvvebTheme.Cart.remove(id, this, function() {
			VvvebTheme.Alert.show('<img height=50 src="' + img + '"> &ensp; <strong>' +  name +'</strong> was removed from cart');
			product.remove();
		});
		
		return false;
	},
	
	addComment : function (e) {
		
		var parameters = $(this).serializeArray();
		
		VvvebTheme.Comments.add(parameters, this, function() { 
				alert("Comment added");
		});
		e.preventDefault();
		
	},	
	
	search : function (e) {
		clearTimeout(window.searchDebounce);
		
		var parameters = $(this).serializeArray();
		
		window.searchDebounce = setTimeout(function () {	
			$("[data-v-component-search]").css("opacity", 0.5);
			VvvebTheme.Search.query(parameters, this, function(data) { 
				$("[data-v-component-search]")[0].outerHTML = data;
		});
		e.preventDefault();
		
		}, 1000);
	},
	
	login : function (e) {
		
		var parameters = $(this).serializeArray();
		
		VvvebTheme.User.login(parameters, this, function(data) { 
			$("[data-v-component-user]")[0].outerHTML = data;
			//	alert("Login");
		});
		e.preventDefault();
		
	}
}	

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();


let urlCache = {};

function preloadUrl(e) {
		delay(() => loadUrl(e, true), 200);
}

function loadUrl(e, preload = false) {
		let element = e.currentTarget;
		let url = element.href;
		let selector = e.data.update;
		//if (!selector) selector = "body";
		console.log(url, preload);
		/*
		console.log(element);
		console.log(e.data);
		console.log(preload);*/
		
		if (!selector) selector = "body";
		
		if  (urlCache.hasOwnProperty(url)) {
			let page =  urlCache[url];
			if (page && !preload) {
				$(selector).replaceWith($(selector, $(page)));
			}
			return;
		} else if (!preload) {
			urlCache[url] = false;//set loading flag
		}
		
		$.ajax({
			dataType : 'html',
			url      : url,
			cache: true,
			success  : function(data) {
				
				//if not preloading or cache loading flag set then update page
				if (!preload || (preload && urlCache.hasOwnProperty(url) && urlCache[url] === false)) {
					let page =  $(data);
					$(selector).replaceWith($(selector, page));
				}
				urlCache[url] = data;
			}
		});
		console.log(selector);
		//let selector = e.
		//if (!selector) selector = "body";
		
		e.preventDefault();
		return false;
}

		
jQuery(document).ready(function() {
	VvvebTheme.Gui.init();
});
/*
if (preloadUrls) {
		for (url in preloadUrls) {
			let link = preloadUrls[url];

			$("body").on("mouseenter",link["link"], link, preloadUrl);
			$("body").on("click",link["link"], link, loadUrl);
		}
}
*/
//ajax url
$("body").on("click", "a[data-url]", function (e) {
	let $this = $(this);
	let selector = this.dataset.selector;
	let url = $this.attr("href");
	console.log(url);
	$.ajax({
		url
	}).done(function (data) {
		let content = $(selector, data);
		if (content.length) {
			$(selector).html(content.html());
		}
	}).fail(function (data) {
		alert(data.responseText);
	});

	e.preventDefault();
})
