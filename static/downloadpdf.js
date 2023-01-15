document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("download-pdf-button").addEventListener("click", function(){
        var pdfPage = document.querySelector('.PDF-Page');
        var pdf = new jsPDF();
        pdf.setPageSize('letter');
        pdf.fromHTML(pdfPage.innerHTML, 15, 15, {
        width: 170
        });
        pdf.save('my-pdf.pdf');
    });
});