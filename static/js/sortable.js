/* Script that allows each colum in a table to be sorted
Found this code at: https://github.com/tofsjonas/sortable 
no changes has been made in the code from the github repo */

document.addEventListener('click', function (e) {
    try {
      // allows for elements inside TH
      function findElementRecursive(element, tag) {
        return element.nodeName === tag ? element : findElementRecursive(element.parentNode, tag)
      }
  
      var down_class = ' dir-d '
      var up_class = ' dir-u '
      var regex_dir = / dir-(u|d) /
      var regex_table = /\bsortable\b/
      var alt_sort = e.shiftKey || e.altKey
      var element = findElementRecursive(e.target, 'TH')
      var tr = findElementRecursive(element, 'TR')
      var table = findElementRecursive(tr, 'TABLE')
  
      function reClassify(element, dir) {
        element.className = element.className.replace(regex_dir, '') + dir
      }
  
      function getValue(element) {
        // If you aren't using data-sort and want to make it just the tiniest bit smaller/faster
        // comment this line and uncomment the next one
        return (
          (alt_sort && element.getAttribute('data-sort-alt')) || element.getAttribute('data-sort') || element.innerText
        )
        // return element.innerText
      }
      if (regex_table.test(table.className)) {
        var column_index
        var nodes = tr.cells
  
        // reset thead cells and get column index
        for (var i = 0; i < nodes.length; i++) {
          if (nodes[i] === element) {
            column_index = element.getAttribute('data-sort-col') || i
          } else {
            reClassify(nodes[i], '')
          }
        }
  
        var dir = down_class
  
        // check if we're sorting up or down, and update the css accordingly
        if (element.className.indexOf(down_class) !== -1) {
          dir = up_class
        }
  
        reClassify(element, dir)
  
        // extract all table rows, so the sorting can start.
        var org_tbody = table.tBodies[0]
  
        // get the array rows in an array, so we can sort them...
        var rows = [].slice.call(org_tbody.rows, 0)
  
        var reverse = dir === up_class
  
        // sort them using custom built in array sort.
        rows.sort(function (a, b) {
          var x = getValue((reverse ? a : b).cells[column_index])
          var y = getValue((reverse ? b : a).cells[column_index])
          return isNaN(x - y) ? x.localeCompare(y) : x - y
        })
  
        // Make a clone without content
        var clone_tbody = org_tbody.cloneNode()
  
        // Build a sorted table body and replace the old one.
        while (rows.length) {
          clone_tbody.appendChild(rows.splice(0, 1)[0])
        }
  
        // And finally insert the end result
        table.replaceChild(clone_tbody, org_tbody)
      }
    } catch (error) {
      // console.log(error)
    }
  })