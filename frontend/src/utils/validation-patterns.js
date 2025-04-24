export const phonePattern = /^\+?[\d\s-]+$/;
export const emailPattern = /^[\d\w._-]+@[\d\w._-]+\.\w{2,}$/i;
export function phoneNumberField(e) {
    const allowedChars = /[+0-9 ]/;
    console.log(e)
    if (!allowedChars.test(String.fromCharCode(e.event.which))) {
        e.event.preventDefault();
    }
}