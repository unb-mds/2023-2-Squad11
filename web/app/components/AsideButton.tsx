import Image, { StaticImageData } from 'next/image';

import Button from './Button';

interface AsideButtonPropsType {
    image: StaticImageData;
    pageName: string;
    innerRef?: (node: any) => void;
    onClick?: () => void;
}


export default function AsideButton({ image, pageName, innerRef, onClick }: AsideButtonPropsType) {
    return (
        <Button innerRef={innerRef} onClick={onClick} className='z-10 flex-col w-full !gap-1 !pb-2 !shadow-none !text-black' name={pageName}>
            <Image
                width={25} height={25}
                src={image} alt={`ícone da página ${pageName}`}
            />
        </Button>
    );
}