// import jsPDF from "jspdf";

document.addEventListener("DOMContentLoaded", () => {
    const downloadButton = getElementById("download-pdf-button");
    console.log(downloadButton);
    downloadButton.addEventListener("click", function(){
        console.log("Click");
        var pdfPage = document.querySelector('.PDF-Page');
        var pdf = new jsPDF();
        pdf.setPageSize('letter');
        pdf.fromHTML(pdfPage.innerHTML, 15, 15, {
        width: 170
    });
        pdf.save('my-pdf.pdf');
    });
});