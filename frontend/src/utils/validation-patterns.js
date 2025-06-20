export const phonePattern = /^\+?[\d\s-]+$/;
export const emailPattern = /^[\d\w._-]+@(?:[\d\w-]+\.)+\w{2,}$/i;
export function phoneNumberField(e) {
    const allowedChars = /[+0-9 \- ]/;
    if (!allowedChars.test(String.fromCharCode(e.event.which))) {
        e.event.preventDefault();
    }
}
export const vatPattern = /^[A-Za-z]{2}[\d]{10,20}$/;