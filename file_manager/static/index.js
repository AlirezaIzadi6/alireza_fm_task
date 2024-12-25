$(document).ready(function() {
    $('#infoModal').on('show.bs.modal', function(event) {
        var clickedButton = $(event.relatedTarget);
        var resourceId = clickedButton.data('id');
        var resourceType = clickedButton.data('type');
        var requestUrl = '';
        if (resourceType == 'folder') {
            requestUrl = getFolderDetailRequestUrl;
        } else {
            requestUrl = getFileDetailRequestUrl;
        }
        requestUrl = requestUrl.replace('123456', resourceId);
        $.ajax({
            url: requestUrl,
            dataType: "json",
            success: function(data) {
                $('#info-modal-body').text('');
                Object.keys(data).forEach(function(key) {
                    var newP = document.createElement('p');
                    newP.textContent = key+': '+data[key];
                    $('#info-modal-body').append(newP);
                });
            }
        });
    });

    $('#renameModal').on('show.bs.modal', function(event) {
        var clickedButton = $(event.relatedTarget);
        var renameButton = $('#renameButton');
        renameButton.data('id', clickedButton.data('id'));
        renameButton.data('type', clickedButton.data('type'));
        $('#renameNewName').val(clickedButton.data('old-name'));
    });

    $('#renameButton').on('click', function(event) {
        var clickedButton = $(this);
        var resourceId = clickedButton.data('id');
        var resourceType = clickedButton.data('type');
        var newName = $('#renameNewName').val();
        var requestUrl = '';
        if (resourceType == 'folder') {
            requestUrl = renameFolderRequestUrl;
        } else {
            requestUrl = renameFileRequestUrl;
        }
        requestUrl = requestUrl.replace('123456', resourceId);
        $.ajax({
            type: 'post',
            url: requestUrl,
            data: {'id': resourceId, 'newName': newName, csrfmiddlewaretoken: csrfToken},
            success: function(result) {
                // Update link to resource:
                var itemLink = $(`#item${resourceId} .col-thumbnail a`);
                var oldItemUrl = itemLink.attr('href');
                var newItemUrl = oldItemUrl.replace(/([^\/]*)$/, newName);
                itemLink.attr('href', newItemUrl);
                // Update name:
                $(`#item${resourceId} .col-name button`).text(newName);
                // Update rename button:
                $(`#item${resourceId} .col-actions .action-rename`).data('old-name', newName);
                $('#renameModal').modal('toggle');
            }, 
            error: function(err) {
                if (err.responseText.length < 100) {
                    alert(err.responseText);
                } else {
                    document.write(err.responseText);
                }
            }
        })
    });

    $('.action-delete').on('click', function(event) {
        var clickedButton = $(this);
        alert('button clicked');
        var resourceId = clickedButton.data('id');
        var resourceType = clickedButton.data('type');
        var isConfirmed = confirm(`Are you sure to delete this ${resourceType}?`);
        if (!isConfirmed) {
            return;
        }
        var requestUrl = '';
        if (resourceType == 'folder') {
            requestUrl = deleteFolderRequestUrl;
        } else {
            requestUrl = deleteFileRequestUrl;
        }
        requestUrl = requestUrl.replace('123456', resourceId);
        $.ajax({
            type: "post",
            url: requestUrl,
            data: {'id': resourceId, csrfmiddlewaretoken: csrfToken},
            success: function(data) {
                window.location.href = currentLocation;
            },
            error: function(data) {
                alert("An error occurred.");
            }
        });
    })
});
