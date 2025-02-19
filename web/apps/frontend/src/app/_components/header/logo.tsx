import logo from '../../../../public/assets/logo.svg'

const Logo = () => {
  return (
      <div className="size-20 bg-gray-200 bg-gradient-to-r from-fuchsia-100 to-purple-700" style={{
          maskImage : `url(${logo.src})`,
          maskSize : 'contain'
        }}
      >
      </div>

  );
};

export default Logo;