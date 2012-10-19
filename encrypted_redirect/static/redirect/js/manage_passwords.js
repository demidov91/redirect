var alphabet = "0123456789АаБбВвГгДдЕеЁёЖжЗзІіЙйКкЛлМмНнОоПпРрСсТтУуЎўФфХхЦцЧчШшЫыЬьЭэЮюЯя"
var encryptedEmptyPlace = AES.encrypt('', '', 256)
var encryptedUrls = [encryptedEmptyPlace]

$(function(){
    addUrlForm()
    $('#save-settings,#restore-settings').tooltip()
    $('#center textarea').autoGrow()
    $('#center textarea').css('width', '100%')
    $('#left input').focus(function(){
        showResultUrlBlock()
    })
    $('#public-url-wrapper .get-activation-link').click(function(){
        showDeleteCookieBlock()
    })
    restoreSettings()
    refreshResultUrl()
})

function genPasswordClick(sender){
    var text = ''
    for( var i=0; i < 16; i++ ){
        text += alphabet.charAt(Math.floor(Math.random() * alphabet.length));
    }
    $(sender).siblings('.password').val(text)
    wasEdited(sender)
}

function refreshResultUrl(){
    $('#result-url textarea').text(redirectUrlStart + encryptedUrls.join(':') + '/')    
}

function wasEdited(sender){
    var editedBlock = $(sender).parent()
    var url = editedBlock.children('.url').val()
    var password = ''
    var index = parseInt(editedBlock.data('index'))
    if($(sender).hasClass('password')){
        password = sender.value
    }
    else if(index != 0){
        password = editedBlock.children('.dot-password').val()        
    }
    if (password == '' && url == '' && index>0 && index == $('#link-password-pairs>*').length){
        $('#link-password-pairs>div:last-child').remove()
        encryptedUrls.pop()    
    }
    else{
        encryptedUrls[index] = AES.encrypt(url, password, 256)
    }
    refreshResultUrl()
}


function addUrlForm(){
    $('#link-password-pairs').append($('#url-password-template').html())
    if($('#link-password-pairs>*').length==5){
        $('#add-url-to-encrypt').css('display', 'none')
    }
    $('#link-password-pairs>div:last-child>input.text-password').change(function(){
        $('#link-password-pairs>div:last-child>input.dot-password').val($('#link-password-pairs>div:last-child>input.text-password').val())
    })
    $('#link-password-pairs>div:last-child>input.dot-password').change(function(){
        $('#link-password-pairs>div:last-child>input.text-password').val($('#link-password-pairs>div:last-child>input.dot-password').val())
    })
    $('#link-password-pairs>div:last-child').data('index', $('#link-password-pairs>div').length)
    $('#link-password-pairs>div:last-child>.get-activation-link').click(function(){
        $('#activation-link textarea').text(activationUrlStart + getActivationLink($(this).parent()))
        $('#activation-link').data('index', $(this).parent().data('index'))
        showActivationLinkBlock()
    })
    encryptedUrls.push(encryptedEmptyPlace)
    $('#save-settings,#restore-settings').attr('disabled', false)
}

function togglePasswords(){
    $('#all-workspace').toggleClass('show-password')
}

//linkBlock - jQuery object for div with url and password
function getActivationLink(linkBlock){
    return linkBlock.data('index') + '/' + linkBlock.children('.dot-password').val() + '/'
}

function passwordChaged(sender){
    $('#save-settings, #restore-settings').attr('disabled', false)
    wasEdited(sender)
    showResultUrlBlock()
}

function showActivationLinkBlock(){
    if($.cookie('cell') == $('#activation-link').data('index')){
        $('#activate-locally').attr('disabled', 'disabled')
    }
    else{
        $('#activate-locally').attr('disabled', false)
    }
    if($('#activation-link').css('display') != 'block'){        
        $('#center>div:visible').fadeOut(function(){$('#activation-link').fadeIn()})       
    }
}

function showResultUrlBlock(){
    $('#activate-locally').attr('disabled', $.cookie('cell') ? false : 'disabled')
    if($('#result-url').css('display') != 'block'){
        $('#center>div:visible').fadeOut(function(){$('#result-url').fadeIn()})   
    }
}

function showDeleteCookieBlock(){
    if($('#delete-cookie').css('display') != 'block'){
        $('#center>div:visible').fadeOut(function(){$('#delete-cookie').fadeIn()})   
    }
}


function saveSettings(){
    $('#save-settings,#restore-settings').tooltip('hide')
    var passwords = []
    $.each($('#link-password-pairs .dot-password'), function(i, password){
        passwords.push(password.value)
    })
    localStorage.passwords = JSON.stringify(passwords)
    $('#save-settings,#restore-settings').attr('disabled', 'disabled')
}
function restoreSettings(){
    $('#save-settings,#restore-settings').tooltip('hide')
    var passwords = JSON.parse(localStorage.passwords)
    if (!passwords){alert('Нічога не было захавана');return;}
    if($('#link-password-pairs>div').length > passwords.length){
        while($('#link-password-pairs>div').length > passwords.length){
            $('#link-password-pairs>div:last-child').remove()
            encryptedUrls.pop()
        }
        $('#add-url-to-encrypt').css('display', 'block')
    }
    for(i = 0; i<Math.min($('#link-password-pairs>div').length, passwords.length); i++){
        $($('#link-password-pairs>div')[i]).find('.password').val(passwords[i])
    }
    for(i=Math.min($('#link-password-pairs>div').length, passwords.length); i<Math.max($('#link-password-pairs>div').length, passwords.length);i++){
        addUrlForm()
        $('#link-password-pairs>div:last-child .password').val(passwords[i])
    }
    $('#save-settings,#restore-settings').attr('disabled', 'disabled')
}

function activateKey(){
    var cell = parseInt($('#activation-link').data('index'))
    $.cookie('cell', cell, {path:cookiePath, expires:1000})
    $.cookie('password', $($('#link-password-pairs>div')[cell-1]).children('.dot-password').val(), {path:cookiePath, expires:1000})
    $('#activate-locally').attr('disabled', 'disabled')
}

function deleteCookies(){
    $.removeCookie('cell', {path:cookiePath})
    $.removeCookie('password', {path:cookiePath})
    $('#delete-cookies').attr('disabled', 'disabled')
}


