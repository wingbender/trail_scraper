function showFavouriteListCreate(t,e){var a=$("#list-favorites-create-modal");e&&a.remove(),a=$("#list-favorites-create-modal"),0===a.length?ListFavoritesCreateListModal.init({literals:t},function(t,e){if(t)throw Error("Error loading template");$(document.body).append(e),$("#list-favorites-create-modal").modal("show")}):a.modal("show")}function isATrailPage(){return/^\d+$/.test(window.location.href.replace("#","").split("-").pop())}var ListFavoritesCreateListModal=function(){function t(t,a){var i=t.literals;return a(null,e(i))}var e=_.template('<div class="modal fade" id="list-favorites-create-modal" tabindex="-1" role="dialog">  <div class="modal-dialog" role="document">    <div class="modal-content">        <div class="modal-header">          <button type="button" class="close" data-dismiss="modal">&times;</button>          <h4 class="modal-title" style="display: inline"><@= newList @></h4>           <span style="color: #aaaaaa; margin-left:10px; font-size: 11px"><@= availableLists @></span>        </div>      <div class="modal-body">      <div class="form-group">        <div  style="display:flex;  flex-direction: row">           <label for="list-favorites-input" class="control-label" style="margin-right: auto!important;"><@= nameList @></label>           <small id="list-favourites-characters" class="form-text text-muted pull-left"><span id="list-favorites-count">0</span>/40</small>        </div>        <input type="text" class="form-control" id="list-favorites-input" placeholder="<@= placeholderList @>" maxlength="40">      </div>      <div class="form-group">           <div class="privacitatButtons btn-group" role="group">             <input class="form-check-input" type="checkbox" value="" id="privacy-checkbox">              <label class="form-check-label" for="privacy-checkbox">             <@= private @>             </label>             <p class="note"></p>         </div>      </div>      <div class="modal-footer">        <button type="button" class="btn btn-primary btn-success" id="list-favorites-save"><@= createList @></button>      </div>    </div>  </div></div></div>');return{init:t}}();$(document).ready(function(){function t(){var t=$("#list-favorites-input").val();if(t){t=t.substr(0,40);var e=!$("#privacy-checkbox").is(":checked"),a={name:t,public:e};isATrailPage()&&(a.spaId=window.location.href.replace("#","").split("-").pop());var i=$.ajax({url:"/wikiloc/create-favorite-list.do?",method:"post",dataType:"json",data:a});i.done(function(t){t.err?400===t.errCode?$("body").trigger("emptyListFavorites",t):403===t.errCode&&$("body").trigger("tooManyListFavorites",t):($("body").trigger("addChildrenListFavorites",t),ga("send",{hitType:"event",eventCategory:"Favorite",eventAction:"create-favorite-list"})),$("#list-favorites-create-modal").modal("hide")})}}$(document).on("shown.bs.modal","#list-favorites-create-modal",function(){$("#list-favorites-input").focus()}),$(document).on("change","#privacy-checkbox",function(t){var e=$(t.currentTarget),a=e.is(":checked");a?$(".note").text(translations.txtPrivacyHelp):$(".note").empty()}),$(document).on("keyup change","#list-favorites-input",function(e){if(this.value.length>=40&&(setTimeout(function(){$("#list-favourites-characters").css("color","black")},1e3),$("#list-favourites-characters").css("color","red")),this.value.length>40)return!1;13===e.which&&($("#list-favorites-create-modal").modal("hide"),t());var a=$("#list-favorites-input").val().length||0;$("#list-favorites-count").text(a)}),$(document).on("click","#list-favorites-save",function(){t()})});