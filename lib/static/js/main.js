$(document).ready(function() {

$(function() {
    var search_source = "";
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }

    $( "#sources, #witnesses, #victims, #perpetrators" )
      .bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB && $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
        if(this.name == "sources"){
            search_source = "/search_source";
        }
        if(this.name == "witnesses"){
            search_source = "/search_witnesses";
        }
        if(this.name == "victims"){
            search_source = "/search_victims";
        }
        if(this.name == "perpetrators"){
            search_source = "/search_perpetrators";
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( search_source, {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          var term = extractLast( this.value );
          if ( term.length < 2 ) {
            return false;
          }
        },
        focus: function() {
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          terms.pop();
          terms.push( ui.item.label );
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
    });

});